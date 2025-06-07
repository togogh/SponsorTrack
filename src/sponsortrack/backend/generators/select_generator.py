from sponsortrack.backend.core.config import settings
from sponsortrack.backend.generators.hf_generator import HuggingFaceGenerator


def select_generator():
    match settings.GENERATOR:
        case "hf":
            return HuggingFaceGenerator()
        case None:
            return None
