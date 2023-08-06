import datetime
import tiktoken

class Response:
    def __init__(self, response_obj, stream=False):
        self._ = response_obj
        self.stream = stream
        self.complete = False
        self._message = ""

        self.gathered = {
            "choices": [{
                "message": {
                    "role": None,
                    "content": ""
                }
            }]
        }

    def __str__(self):
        return "<assistant> %s" % self.message

    def __len__(self):
        """ Returns the length of the text, in characters """
        return len(self.message)

    def get_tokens(self):
        """ Returns the length of the content, in tokens """
        tokenizer = tiktoken.get_encoding("cl100k_base")

        return len(tokenizer.encode(self.message))

    @property
    def rsp(self):
        if self.stream:
            return self.gathered
        else:
            return self._

    @property
    def obj(self):
        return {
            "role": self.choices[0]["message"]["role"],
            "content": self.choices[0]["message"]["content"]
        }

    @property
    def id(self):
        return self.rsp["id"]

    @property
    def created(self):
        return datetime.fromtimestamp(self.rsp["created"])

    @property
    def usage(self):
        return self.rsp["usage"]

    @property
    def model(self):
        return self.rsp["model"]

    @property
    def choices(self):
        return self.rsp["choices"]

    @property
    def message(self):
        """ Returns the message from the first generated choice """

        if self.complete:
            return self.gathered["choices"][0]["message"]["content"]

        if self.stream:
            return self._message_stream

        # The first generation or so typically has newlines, so
        # I'm .strip()'ing them out.
        return self.choices[0]["message"]["content"].strip()

    @property
    def _message_stream(self):
        """ Special handling for streams only """

        for resp in self._:
            self.gathered["id"] = resp["id"]
            self.gathered["model"] = resp["model"]

            delta = resp["choices"][0]["delta"]

            if "role" in delta:
                self.gathered["choices"][0]["message"]["role"] = delta["role"]

            if "content" in delta:
                segment = delta["content"]

                self.gathered["choices"][0]["message"]["content"] += segment

                yield segment
            else:
                yield ""

            self.gathered["choices"][0]["finished_reason"] = \
                resp["choices"][0]["finish_reason"]

        self.complete = True
