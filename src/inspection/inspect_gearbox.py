from ..models.gearbox_model import Gearbox

test_files = [
    'experiments/set1x.jpg',
    'experiments/set2x.jpg',
    'experiments/set3x_notooth.jpg',
    'experiments/set3x_notooth_rot.jpg',
    'experiments/set4x_worn.jpg',
    'experiments/set5x.jpg',
    'experiments/set6x.jpg'
]

for image in test_files:
    gearbox = Gearbox(image)
    gearbox.inspect()
    gearbox.report()