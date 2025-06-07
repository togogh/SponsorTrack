from sponsortrack.config import GENERATOR
from sponsortrack.backend.generators.hf_generator import HuggingFaceGenerator


def select_generator():
    match GENERATOR:
        case "hf":
            return HuggingFaceGenerator()
        case None:
            return None
