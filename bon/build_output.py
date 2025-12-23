import json
import shutil
import subprocess
from pathlib import Path

from .config import HOME, MODULE_NAME, TEX_SEP, TMP_PATH
from .preview import make_tex_code

root = Path(HOME) / MODULE_NAME
tmp_dir = Path(TMP_PATH)
output_base = Path(HOME) / MODULE_NAME / "output"

tmp_dir.mkdir(parents=True, exist_ok=True)
output_base.mkdir(parents=True, exist_ok=True)

for json_path in sorted(root.rglob("*.json")):
    if json_path.name == "puids.json":
        continue

    rel = json_path.relative_to(root)
    out_dir = output_base / rel.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    db_content = json.loads(json_path.read_text(encoding="utf-8"))
    puid = rel.as_posix()

    tex = make_tex_code(db_content, puid, TEX_SEP)
    jobname = str(rel).replace("/", "-").replace("\\", "-")
    tmp_tex = tmp_dir / (jobname + ".tex")
    tmp_tex.write_text(tex, encoding="utf-8")

    subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", tmp_tex.name], cwd=tmp_dir
    )

    pdf = tmp_tex.with_suffix(".pdf")
    if pdf.exists():
        shutil.copy2(pdf, out_dir / (rel.stem + ".pdf"))

    subprocess.run(["latexmk", "-c", tmp_tex.name], cwd=tmp_dir)

print("Done. PDFs are in:", output_base)
