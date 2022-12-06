import pytest
import cv2
from ...src.models.gearbox_model import Gearbox, Components

class TestAllPass1:
    "No faulty parts"

    @pytest.fixture
    def gearbox(self):
        gearbox = Gearbox()
        image = cv2.imread('tests/images/raw/final_all_good.jpg', cv2.IMREAD_GRAYSCALE)
        gearbox.inspect(image)
        return gearbox

    def test_top_casing_passes(self, gearbox):
        assert gearbox.components["Top Casing"].status["code"] == 0

    def test_bottom_casing_passes(self, gearbox):
        assert gearbox.components["Bottom Casing"].status["code"] == 0

    def test_small_gear_passes(self, gearbox):
        assert gearbox.components["Small Gear"].status["code"] == 0

    def test_large_gear_passes(self, gearbox):
        assert gearbox.components["Large Gear"].status["code"] == 0

    def test_gearbox_passes(self, gearbox):
        assert gearbox.status["code"] == 0

class TestTopCasingBottomCasingSmallAndLargeGearFailMissingTooth1:
    "Holes on both casings milled to large, tooth missing on both gears"

    @pytest.fixture
    def gearbox(self):
        gearbox = Gearbox()
        image = cv2.imread('tests/images/raw/final_bad_casing_missing_tooth.jpg', cv2.IMREAD_GRAYSCALE)
        gearbox.inspect(image)
        return gearbox

    def test_top_casing_passes(self, gearbox):
        assert gearbox.components["Top Casing"].status["code"] == 3

    def test_bottom_casing_passes(self, gearbox):
        assert gearbox.components["Bottom Casing"].status["code"] == 3

    def test_small_gear_fails(self, gearbox):
        assert gearbox.components["Small Gear"].status["code"] == 2

    def test_large_gear_fails(self, gearbox):
        assert gearbox.components["Large Gear"].status["code"] == 2

    def test_gearbox_fails(self, gearbox):
        assert gearbox.status["code"] == 15

class TestTopCasingBottomCasingSmallAndLargeGearFailWorn1:
    "Holes on both casings milled to large, teeth worn on both gears"

    @pytest.fixture
    def gearbox(self):
        gearbox = Gearbox()
        image = cv2.imread('tests/images/raw/final_bad_casing_worn_teeth.jpg', cv2.IMREAD_GRAYSCALE)
        gearbox.inspect(image)
        return gearbox

    def test_top_casing_passes(self, gearbox):
        assert gearbox.components["Top Casing"].status["code"] == 3

    def test_bottom_casing_passes(self, gearbox):
        assert gearbox.components["Bottom Casing"].status["code"] == 3

    def test_small_gear_fails(self, gearbox):
        assert gearbox.components["Small Gear"].status["code"] == 1

    def test_large_gear_fails(self, gearbox):
        assert gearbox.components["Large Gear"].status["code"] == 1

    def test_gearbox_fails(self, gearbox):
        assert gearbox.status["code"] == 15

class TestBlank1:
    "Shuttle with no kitting tray"

    @pytest.fixture
    def gearbox(self):
        gearbox = Gearbox()
        image = cv2.imread('tests/images/raw/blank_1.jpg', cv2.IMREAD_GRAYSCALE)
        gearbox.inspect(image)
        return gearbox

    def test_top_casing_fails(self, gearbox):
        assert gearbox.components["Top Casing"].status["code"] == 99

    def test_bottom_casing_fails(self, gearbox):
        assert gearbox.components["Bottom Casing"].status["code"] == 99

    def test_small_gear_fails(self, gearbox):
        assert gearbox.components["Small Gear"].status["code"] == 99

    def test_large_gear_fails(self, gearbox):
        assert gearbox.components["Large Gear"].status["code"] == 99

    def test_gearbox_fails(self, gearbox):
        assert gearbox.status["code"] == 15