import pytest
from ...src.models.gearbox_model import Gearbox, Components

class TestSet1x:
    "No faulty parts"

    @pytest.fixture
    def gearbox(self):
        gearbox = Gearbox('tests/images/raw/set1x.jpg')
        gearbox.inspect()
        return gearbox

    def test_top_casing_passes(self, gearbox):
        assert gearbox.components["Top Casing"].status["code"] == 0

    def test_bottom_casing_passes(self, gearbox):
        assert gearbox.components["Bottom Casing"].status["code"] == 0

    def test_small_gear_passes(self, gearbox):
        assert gearbox.components["Small Gear"].status["code"] == 0

    def test_large_gear_passes(self, gearbox):
        assert gearbox.components["Large Gear"].status["code"] == 0

class TestSet2x:
    "No faulty parts"

    @pytest.fixture
    def gearbox(self):
        gearbox = Gearbox('tests/images/raw/set2x.jpg')
        gearbox.inspect()
        return gearbox

    def test_top_casing_passes(self, gearbox):
        assert gearbox.components["Top Casing"].status["code"] == 0

    def test_bottom_casing_passes(self, gearbox):
        assert gearbox.components["Bottom Casing"].status["code"] == 0

    def test_small_gear_passes(self, gearbox):
        assert gearbox.components["Small Gear"].status["code"] == 0

    def test_large_gear_passes(self, gearbox):
        assert gearbox.components["Large Gear"].status["code"] == 0

class TestSet3x_notooth:
    "Tooth missing on both gears"

    @pytest.fixture
    def gearbox(self):
        gearbox = Gearbox('tests/images/raw/set3x_notooth.jpg')
        gearbox.inspect()
        return gearbox

    def test_top_casing_passes(self, gearbox):
        assert gearbox.components["Top Casing"].status["code"] == 0

    def test_bottom_casing_passes(self, gearbox):
        assert gearbox.components["Bottom Casing"].status["code"] == 0

    def test_small_gear_passes(self, gearbox):
        assert gearbox.components["Small Gear"].status["code"] == 2

    def test_large_gear_passes(self, gearbox):
        assert gearbox.components["Large Gear"].status["code"] == 2

class TestSet3x_notooth_rot:
    "Tooth missing on both gears"

    @pytest.fixture
    def gearbox(self):
        gearbox = Gearbox('tests/images/raw/set3x_notooth_rot.jpg')
        gearbox.inspect()
        return gearbox

    def test_top_casing_passes(self, gearbox):
        assert gearbox.components["Top Casing"].status["code"] == 0

    def test_bottom_casing_passes(self, gearbox):
        assert gearbox.components["Bottom Casing"].status["code"] == 0

    def test_small_gear_passes(self, gearbox):
        assert gearbox.components["Small Gear"].status["code"] == 2

    def test_large_gear_passes(self, gearbox):
        assert gearbox.components["Large Gear"].status["code"] == 2

class TestSet4x_worn:
    "Teeth worn on both gears"

    @pytest.fixture
    def gearbox(self):
        gearbox = Gearbox('tests/images/raw/set4x_worn.jpg')
        gearbox.inspect()
        return gearbox

    def test_top_casing_passes(self, gearbox):
        assert gearbox.components["Top Casing"].status["code"] == 0

    def test_bottom_casing_passes(self, gearbox):
        assert gearbox.components["Bottom Casing"].status["code"] == 0

    def test_small_gear_passes(self, gearbox):
        assert gearbox.components["Small Gear"].status["code"] == 1

    def test_large_gear_passes(self, gearbox):
        assert gearbox.components["Large Gear"].status["code"] == 1

class TestSet5x:
    "No faulty parts"

    @pytest.fixture
    def gearbox(self):
        gearbox = Gearbox('tests/images/raw/set5x.jpg')
        gearbox.inspect()
        return gearbox

    def test_top_casing_passes(self, gearbox):
        assert gearbox.components["Top Casing"].status["code"] == 0

    def test_bottom_casing_passes(self, gearbox):
        assert gearbox.components["Bottom Casing"].status["code"] == 0

    def test_small_gear_passes(self, gearbox):
        assert gearbox.components["Small Gear"].status["code"] == 0

    def test_large_gear_passes(self, gearbox):
        assert gearbox.components["Large Gear"].status["code"] == 0

class TestSet6x:
    "No faulty parts"

    @pytest.fixture
    def gearbox(self):
        gearbox = Gearbox('tests/images/raw/set6x.jpg')
        gearbox.inspect()
        return gearbox

    def test_top_casing_passes(self, gearbox):
        assert gearbox.components["Top Casing"].status["code"] == 0

    def test_bottom_casing_passes(self, gearbox):
        assert gearbox.components["Bottom Casing"].status["code"] == 0

    def test_small_gear_passes(self, gearbox):
        assert gearbox.components["Small Gear"].status["code"] == 0

    def test_large_gear_passes(self, gearbox):
        assert gearbox.components["Large Gear"].status["code"] == 0