"""The Kurzgesagt Package"""
import os
import webbrowser
from random import shuffle

__version__ = "1.1.2"

ALPHA = list("Z(Uf!tEn:kGIAismuWeK?)oFwcyrzXRM JqOBNH,aDTgQxSCljvhpdbYPVL.")
MESSAGE = "NujR!hioe(FEwiMc)sMAE!WoWsZWh At HMcWLfmkyKoM,MC)dMAEZWrxAuwKRTjWnrgeUFkmr:E)ofM miZMsiEh su HMpOZclkCXxWyiI)EM)Ur!hiMAomccuMcWleXbnxiMFvuyWM!v:i iycoyRiAMtSoo)LdXcWhCHwWM!v:i GWAs,DeRFiZS FiGwrsWiA,TWM!WMmiLROURc?mrki,XEqEiMimcWMc)m'yermAiED fverkaAkymUwycv!A)EMGWtS)h.ME)"
MAGIC = 12021055047710724565076463829

print(
    "Dear friend, thanks for starting this puzzle journey with me! There are still some steps ahead of you. Good luck!"
)


def gauss(prime: int = 2) -> None:
    """Gauss what."""

    if MAGIC % prime == 0 and not MAGIC == prime:  # check for the correct prime factor
        k = str(MAGIC // prime) + "".join(list(map(str, [ord(c) for c in os.name])))
        msg = ""
        for n, c in enumerate(MESSAGE):
            if c in ALPHA:
                c = ALPHA[(ALPHA.index(c) + int(k[n % len(k)])) % len(ALPHA)]
            msg += c
        print(msg)
        random()
    else:
        print("Nope, sorry. You have to find Gauß first to solve this puzzle.")


def random() -> None:
    """Pull up a random video from Kurzgesagt."""

    video_urls = [
        "https://www.youtube.com/watch?v=75d_29QWELk",  # How to change
        "https://www.youtube.com/watch?v=LxgMdjyw8uw",  # We WILL fix climate change
        "https://www.youtube.com/watch?v=yiw6_JakZFc",  # Can you fix climate change?
        "https://www.youtube.com/watch?v=JXeJANDKwDc",  # The tail end
        "https://www.youtube.com/watch?v=WPPPFqsECz0",  # Dissatisfaction
        "https://www.youtube.com/watch?v=n3Xv_g3g-mA",  # Loneliness
    ]
    shuffle(video_urls)

    webbrowser.open(video_urls[0], new=1, autoraise=True)
