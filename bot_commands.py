import random
from PIL import Image

def random_champions(champions: set, n: int, bans: set = set()) -> set:
    """Returns a set of n random champions, after removing bans"""

    if n <= 0:
        n = 1
    elif n > len(champions):
        n = len(champions)

    available = champions - bans

    # add banned champions back to pool if not enough available champions
    if len(available) < n:
        missing = n - len(available) 
        available.update(random.sample(list(bans), missing))

    selected = set(random.sample(list(available), n))

    return selected


def create_grid(champions) -> Image:
    """Create and save champion grid"""
    
    icons = []
    COLUMNS = 6
    for champion in champions:
        icon = Image.open(f"icons/{champion}.png")
        icons.append(icon)
    
    if len(champions) % 6 == 0:
        rows = int(len(champions)/6)
    else:
        # allow for one extra row for remaining champions
        rows = len(champions) // 6 + 1
    
    if len(champions) < COLUMNS:
        COLUMNS = len(champions)
    
    width, height = icons[0].size
    grid = Image.new('RGB', size=(COLUMNS*width, rows*height))
    
    for i, img in enumerate(icons):
        grid.paste(img, box=(i%COLUMNS*width, i//COLUMNS*height))
    
    try:
        grid.save("grid.png")
        return True
    except:
        return False