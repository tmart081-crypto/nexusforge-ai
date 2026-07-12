import io

from PIL import Image

from services import image_service


def _png_bytes(size=(100, 100), color="red"):
    buf = io.BytesIO()
    Image.new("RGB", size, color=color).save(buf, format="PNG")
    buf.seek(0)
    return buf


def test_load_image_rejects_corrupt_file():
    result = image_service.load_image(io.BytesIO(b"not an image, just garbage bytes"))
    assert result["ok"] is False
    assert "corrupt" in result["error"].lower()


def test_load_image_accepts_valid_png():
    result = image_service.load_image(_png_bytes())
    assert result["ok"] is True
    assert result["result"].size == (100, 100)
    assert result["result"].mode == "RGB"


def test_load_image_rejects_oversized_image():
    result = image_service.load_image(_png_bytes(size=(5000, 10)))
    assert result["ok"] is False
    assert "too large" in result["error"].lower()


def test_visual_question_answer_rejects_empty_question():
    result = image_service.visual_question_answer(Image.new("RGB", (10, 10)), "   ")
    assert result["ok"] is False
    assert "question" in result["error"].lower()
