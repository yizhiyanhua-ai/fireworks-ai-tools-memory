# Tool Taxonomy

Recommended memory scopes:

- `single-cli`: one CLI with repeated quirks, like `ncm-cli`
- `paired-toolchain`: two tools that form one stable path, like `yt-dlp+mpv`
- `service-runtime`: tools with daemon or app state, like `paseo`
- `scriptable-publisher`: tools that combine API + local preprocessing, like `lark-cli`

Preferred rule:

If the lesson is primarily about runtime behavior, environment constraints, auth, process lifecycle, or script reuse, store it as tool memory first.
