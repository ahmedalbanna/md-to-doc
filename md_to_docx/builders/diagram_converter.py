import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from ..models import DocumentMetadata


PLANTUML_JAR_NAMES = ["plantuml.jar", "plantuml"]
MERMAID_CLI_NAMES = ["mmdc", "mermaid-cli"]


class DiagramConverter:
    def __init__(self, metadata: DocumentMetadata, diagrams_dir: str = None):
        self.metadata = metadata
        self.diagrams_dir = diagrams_dir or tempfile.mkdtemp()

    def convert_plantuml(self, code: str, output_format: str = "png") -> str:
        output_path = os.path.join(self.diagrams_dir, f"diagram_{abs(hash(code))}.{output_format}")
        if os.path.exists(output_path):
            return output_path

        plantuml_path = self._find_plantuml()
        if not plantuml_path:
            return ""

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".puml", delete=False, dir=self.diagrams_dir
            ) as f:
                f.write("@startuml\n")
                f.write(code)
                if not code.strip().endswith("@enduml"):
                    f.write("\n@enduml")
                f.flush()
                input_path = f.name

            cmd = ["java", "-jar", plantuml_path, "-t" + output_format, input_path, "-o", self.diagrams_dir]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            base_name = os.path.splitext(os.path.basename(input_path))[0]
            expected = os.path.join(self.diagrams_dir, f"{base_name}.{output_format}")
            if os.path.exists(expected):
                os.rename(expected, output_path)
            os.unlink(input_path)

            if os.path.exists(output_path):
                return output_path
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            pass

        return ""

    def convert_mermaid(self, code: str, output_format: str = "png") -> str:
        output_path = os.path.join(self.diagrams_dir, f"mermaid_{abs(hash(code))}.{output_format}")
        if os.path.exists(output_path):
            return output_path

        mmdc_path = self._find_mermaid_cli()
        if not mmdc_path:
            return ""

        try:
            mmd_content = code
            if not code.strip().startswith(("graph ", "sequenceDiagram", "classDiagram",
                                           "stateDiagram", "erDiagram", "flowchart",
                                           "gantt", "pie", "gitgraph", "mindmap")):
                return ""

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".mmd", delete=False, dir=self.diagrams_dir
            ) as f:
                f.write(mmd_content)
                f.flush()
                input_path = f.name

            cmd = [mmdc_path, "-i", input_path, "-o", output_path, "-f"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            os.unlink(input_path)

            if os.path.exists(output_path):
                return output_path
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            pass

        return ""

    def _find_plantuml(self) -> str:
        for name in PLANTUML_JAR_NAMES:
            if shutil.which(name):
                return name
        for name in PLANTUML_JAR_NAMES:
            if name.endswith(".jar"):
                path = os.path.expanduser(f"~/{name}")
                if os.path.exists(path):
                    return path
        try:
            result = subprocess.run(["which", "plantuml"], capture_output=True, text=True)
            if result.stdout.strip():
                return result.stdout.strip()
        except FileNotFoundError:
            pass
        return ""

    def _find_mermaid_cli(self) -> str:
        for name in MERMAID_CLI_NAMES:
            if shutil.which(name):
                return name
        try:
            result = subprocess.run(["which", "mmdc"], capture_output=True, text=True)
            if result.stdout.strip():
                return result.stdout.strip()
        except FileNotFoundError:
            pass
        try:
            result = subprocess.run(["npx", "--yes", "mmdc", "--version"],
                                    capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return "npx --yes mmdc"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return ""

    def cleanup(self):
        if os.path.exists(self.diagrams_dir):
            shutil.rmtree(self.diagrams_dir, ignore_errors=True)