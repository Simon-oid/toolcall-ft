/* judge: levels 1 and 2 of a tool call, decided by cMCP's own parser and
 * JSON Schema validator -- the code the real server runs on tools/call.
 *
 *   judge TOOLS.json < calls.jsonl > verdicts.jsonl
 *
 * TOOLS.json  the tools as servers list them: {"tools":[{"name",
 *             "inputSchema"}, ...]} (cmcp-inspect -j output, merged).
 * stdin       one JSON *string* per line: the text the model emitted as
 *             its call, e.g. "{\"name\":\"fs_read\",\"arguments\":{...}}".
 * stdout      one object per line, in order:
 *   {"json":bool,"name":str|null,"known":bool,"schema":bool,
 *    "error":{"path","keyword","message"}|null}
 *
 *   json    the text parses (strict RFC 8259) to an object with a string
 *           "name" and an object "arguments"
 *   known   "name" is one of the tools
 *   schema  known, and "arguments" validates against its inputSchema
 *
 * Exit 2 on bad usage or a bad TOOLS file; a bad input line is a verdict,
 * never a crash.
 */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "cmcp.h"
#include "cmcp_json.h"
#include "cmcp_schema.h"

static char *slurp(const char *path, size_t *len) {
    FILE *f = fopen(path, "rb");
    if (!f) return NULL;
    char *buf = NULL;
    size_t cap = 0, n = 0;
    for (;;) {
        if (n + 4096 > cap) {
            cap = cap ? cap * 2 : 65536;
            char *p = realloc(buf, cap);
            if (!p) { free(buf); fclose(f); return NULL; }
            buf = p;
        }
        size_t r = fread(buf + n, 1, cap - n, f);
        n += r;
        if (r == 0) break;
    }
    fclose(f);
    *len = n;
    return buf;
}

static const cmcp_json_t *find_schema(const cmcp_json_t *tools, const char *name, size_t len) {
    size_t n = cmcp_json_array_len(tools);
    for (size_t i = 0; i < n; i++) {
        const cmcp_json_t *t = cmcp_json_array_at(tools, i);
        const cmcp_json_t *nm = cmcp_json_object_get(t, "name");
        if (nm && nm->type == CMCP_JSON_STRING && cmcp_json_string_len(nm) == len &&
            memcmp(cmcp_json_string(nm), name, len) == 0)
            return cmcp_json_object_get(t, "inputSchema");
    }
    return NULL;
}

static void put_bool(cmcp_json_t *o, const char *k, int b) {
    cmcp_json_object_set(o, k, cmcp_json_new_bool(b));
}

/* The verdict for one call text. Caller owns the result. */
static cmcp_json_t *judge_one(const cmcp_json_t *tools, const char *text, size_t len) {
    cmcp_json_t *out = cmcp_json_new_object();
    cmcp_json_t *call = cmcp_json_parse(text, len);
    const cmcp_json_t *name = call ? cmcp_json_object_get(call, "name") : NULL;
    const cmcp_json_t *args = call ? cmcp_json_object_get(call, "arguments") : NULL;
    int json_ok = call && call->type == CMCP_JSON_OBJECT && name && name->type == CMCP_JSON_STRING &&
                  args && args->type == CMCP_JSON_OBJECT;
    put_bool(out, "json", json_ok);
    cmcp_json_object_set(out, "name",
        name && name->type == CMCP_JSON_STRING
            ? cmcp_json_new_string_n(cmcp_json_string(name), cmcp_json_string_len(name))
            : cmcp_json_new_null());
    const cmcp_json_t *schema = json_ok
        ? find_schema(tools, cmcp_json_string(name), cmcp_json_string_len(name)) : NULL;
    put_bool(out, "known", schema != NULL);
    cmcp_json_t *error = cmcp_json_new_null();
    int schema_ok = 0;
    if (schema) {
        cmcp_schema_error_t err;
        int rc = cmcp_schema_validate(schema, args, &err);
        schema_ok = rc == CMCP_OK;
        if (!schema_ok) {
            cmcp_json_t *e = cmcp_schema_error_to_json(&err);
            if (e) { cmcp_json_free(error); error = e; }
        }
        cmcp_schema_error_clear(&err);
    }
    put_bool(out, "schema", schema_ok);
    cmcp_json_object_set(out, "error", error);
    cmcp_json_free(call);
    return out;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: judge TOOLS.json < calls.jsonl\n");
        return 2;
    }
    size_t tlen = 0;
    char *tbuf = slurp(argv[1], &tlen);
    cmcp_json_t *doc = tbuf ? cmcp_json_parse(tbuf, tlen) : NULL;
    free(tbuf);
    const cmcp_json_t *tools = doc ? cmcp_json_object_get(doc, "tools") : NULL;
    if (!tools || tools->type != CMCP_JSON_ARRAY) {
        fprintf(stderr, "judge: %s is not {\"tools\": [...]}\n", argv[1]);
        cmcp_json_free(doc);
        return 2;
    }
    char *line = NULL;
    size_t cap = 0;
    ssize_t n;
    while ((n = getline(&line, &cap, stdin)) >= 0) {
        while (n > 0 && (line[n - 1] == '\n' || line[n - 1] == '\r')) line[--n] = '\0';
        cmcp_json_t *s = cmcp_json_parse(line, (size_t)n);
        cmcp_json_t *v = (s && s->type == CMCP_JSON_STRING)
            ? judge_one(tools, cmcp_json_string(s), cmcp_json_string_len(s))
            : judge_one(tools, "", 0);           /* not a JSON string: not a call */
        char *txt = cmcp_json_emit(v);
        if (txt) { fputs(txt, stdout); fputc('\n', stdout); free(txt); }
        cmcp_json_free(v);
        cmcp_json_free(s);
    }
    free(line);
    cmcp_json_free(doc);
    return 0;
}
