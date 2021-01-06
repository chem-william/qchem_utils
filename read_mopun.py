import re
import numpy as np
from tqdm import tqdm


def is_float(element: str) -> bool:
    try:
        float(element)
        return True

    except ValueError:
        return False


with open("./DALTON.MOPUN") as mopun:
    mopun.readline()  # Skip the header
    lines = mopun.readlines()

    data = []
    count = 0
    for idx, line in tqdm(enumerate(lines)):
        line = line.split()

        for idx, item in enumerate(line):
            if len(item) > 18:  # Formatting of MOPUN is screwed...
                item_split = re.split("(-)", item.strip())

                skip = False
                for idx in np.arange(len(item_split)):
                    if not skip:
                        if is_float(item_split[idx]):
                            print(item_split[idx])
                            data.append(float(item_split[idx]))

                        if item_split[idx] == "-":
                            count += 1
                            data.append(
                                float("".join([item_split[idx], item_split[idx + 1]]))
                            )
                            skip = True
                    else:
                        skip = False
                        continue
            else:
                data.append(float(item))
    data = np.array(data)

    data = data.reshape((128, 128))
