#!/usr/bin/env python

import re
import sys

regexp = r"([^a-z^\s^'^-])|(?:^|[^a-z])['-]|['-](?:^|[^a-z])|'*(?<![a-z-])(?:a|an|the|and|or|as|of|in|on|yet|our|than|then|however|at|but|was|were|which|there|this|that|thus|we|to|for|is|are|where|have|has|been|since|with|such|another|also|by|often|can|could|so|from|its|via|will|hence|should|would|shall|what|although|these|those|do|does|did|under|above|else|if|while|when|who|based|way|very|many|much|due|because|onto|into|out|finally|their|they|may|might|up|down|either|neither|nor|within|according|others|about|therefore|no|not|towards|beyond|behind|over|how|both|without|other|another|more|most|moreover|be|furthermore|why|paper|focuses|well|must|consider|using|used|commonly|some|given|among|able|present|his|her|he|she|obtained|makes|give|make|further|use|introduce|employ|uses|show|allows|gives|introduces|considers|through|take|takes|enable|enables|allow|every|each|called|provide|provides|cannot|allowing|even|though|after|around|upon|you|new)(?![a-z-])'*"

for line in sys.stdin:
    for combination in re.split(regexp, line):
        if combination is None:
            continue

        combination = combination.strip()

        if len(re.split(r"\s+", combination)) >= 2: # считаем за темы пары слов больше 2
            print(combination + ",1")
