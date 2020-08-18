# SubtitleLemmatizer

Subtitle Lemmatizer is API for providing fully lemmatized script for particular episode/season. It downloads needed scripts using OpenSubtitles API, parses it, lemmatizes it using detutschtextarchiv API. Then by combining time codes from subtitles and lemmas creates a json time codes, containing each lemmatized lemma.