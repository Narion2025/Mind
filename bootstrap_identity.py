import os
import yaml
from modules.marker_grapper import MarkerGrapper
from modules.marker_selfwriter import MarkerSelfwriter
from modules.color_utils import do_color_test, get_marker_sets_for


def bootstrap_identity(name: str):
    farbe = do_color_test()
    reinforce, contrast = get_marker_sets_for(farbe)

    choice = input("Verstärkend (v) oder kontrastierend (k)?: ").strip().lower()
    include_sets = [reinforce] if choice != "k" else [contrast]

    filter_tags = []

    config = {
        "name": name,
        "farbe": farbe,
        "marker_view": {
            "include_sets": include_sets,
            "filter_tags": filter_tags,
        },
    }

    os.makedirs(name, exist_ok=True)
    path = os.path.join(name, f"{farbe}.yaml")
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, allow_unicode=True)

    grapper = MarkerGrapper(include_sets=include_sets, filter_tags=filter_tags)
    selfwriter = MarkerSelfwriter(os.path.join(name, "self_written"))
    return grapper, selfwriter


if __name__ == "__main__":
    g, w = bootstrap_identity("Assistent_Kairos")
    print("Bootstrap abgeschlossen. MarkerGrapper und MarkerSelfwriter initialisiert")
