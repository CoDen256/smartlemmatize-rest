# SubtitleLemmatizer

Subtitle Lemmatizer is API for providing fully lemmatized script for particular episode/season. It downloads needed 
scripts using OpenSubtitles API, parses it, lemmatizes it using detutschtextarchiv API. 
Then by combining time codes from subtitles and lemmas creates a json time codes, containing each lemmatized word.

All computations, parsing and data handling first were created by Chain Of Responsibility, but then everything 
was rearranged as pipelines.
# Pipelines
Pipelines were created as a tool to pass a data between different handlers with specific flow.
E.g. A => B => C => D will be expressed as a sequence of pipelines connected to each other. like : a.to(b).to(c).to(d)
If a starts executing the query, it will receive, then upon execution it will be passed to other handlers. Each pipeline
waits for all incoming pipelines to pass their results, to start own execution.
E.g. A => B, and C => B, (looks like a.to(b);c.to(b) OR b.from_(a, c))
First executes A, then C and then B based on the outputs of incoming lines.

The idea to build condition pipelines in runtime in dependence on conditions was rejected, because the in-/outcoming 
pipelines lists should be deterministic. If the connections are being established upon execution of condition, then, 
all branches, that are executed on one condition branch or another should have been connected in runtime as well, 
which brings a lot of problems.

Instead the Connector was introduced, which operates on low level pipeline connections, and just calls functions
of their connection
