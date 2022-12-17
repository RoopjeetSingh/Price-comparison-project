import json
from PIL import Image

f = open('sprouts.json')
sprouts_data = json.load(f)


def get_from_sprouts(product: str, keywords: tuple[str]):
    if keywords:
        for i, v in sprouts_data.items():
            for j in keywords:
                if j.capitalize() not in i:
                    break
            else:
                print(i, v)
                return {i: v}
    else:
        for i, v in sprouts_data.items():
            for j in product.split():
                if j.capitalize() not in i:
                    break
            else:
                print(i, v)
                return {i: v}
    return {}


f.close()
if __name__ == "__main__":
    sprouts_result = get_from_sprouts("nature's own whole wheat bread", tuple("nature's own whole wheat bread".split()))
    for k, vs in sprouts_result.items():
        img_product = Image.open(vs[2])
        img_product.show()
