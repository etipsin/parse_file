from typing import Iterable, Dict


def parse_file(path: str) -> Iterable[Dict[str, str]]:
    with open(path, "r") as f:
        document = {}
        tag = None

        for line in f.readlines():

            if line.strip().startswith("#"):
                # comment
                continue

            if not line.strip():
                # empty line
                if not document:
                    # multiply empty line
                    continue

                document[tag] = "\n".join(document[tag])

                yield document

                document = {}
                tag = None

                continue

            if line.startswith(" "):
                # no tag
                document[tag].append(line.strip())
            else:
                # tag
                new_tag, data = line.split(":", maxsplit=1)

                if tag and tag != new_tag:
                    # tag change
                    document[tag] = "\n".join(document[tag])

                if new_tag not in document:
                    document[new_tag] = []

                # changed:        ***@afrinic.net 20050205
                # source:         AFRINIC
                # changed:        ***@ripe.net 20050202
                try:
                    document[new_tag].append(data.strip())
                except AttributeError:
                    document[new_tag] = [document[new_tag], data.strip()]

                tag = new_tag

        if not document:
            return

        document[tag] = "\n".join(document[tag])

        yield document
