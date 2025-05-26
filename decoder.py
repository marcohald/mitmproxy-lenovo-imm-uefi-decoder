import json
import base64
import EfiCompressor
from mitmproxy import contentviews, flow, http, ctx
from mitmproxy.addonmanager import Loader


PARSE_ERROR = object()

def parse_json(s: bytes) -> any:
    try:
        return json.loads(s.decode("utf-8"))
    except ValueError:
        return PARSE_ERROR




def uefi_to_json(uefi: str) -> str:
    data = base64.b64decode(uefi)
    efi_text = EfiCompressor.FrameworkDecompress(data, len(data)).decode("utf-8")
    return efi_text


class ASUView(contentviews.View):
    name = "asu decoded"
    syntax_highlight = "xml"
    
    
    def __call__(
        self,
        data: bytes,
        *,
        content_type: str | None = None,
        flow: flow.Flow | None = None,
        http_message: http.Message | None = None,
        **unknown_metadata,
    ) -> contentviews.TViewResult:
        if content_type and  content_type == "application/json":
            json_data = flow.request.json()
            if json_data["FileName"]:
                filename = json_data["FileName"]

                print(filename)
                #print(parse_json(data))
                if filename == "asu_update.efi" or  filename == "config.efi":
                    data_parsed = parse_json(data)
                    data_parsed = uefi_to_json(data_parsed["Content"])
                    #print(data_parsed)

                    if data_parsed is not PARSE_ERROR:
                        return "Lenovo ASU View", contentviews.format_text(data_parsed)
                if filename == "config_log":
                    data_parsed = parse_json(data)
                    
                    return "Lenovo ASU View", contentviews.format_text(base64.b64decode(data_parsed["Content"]))



    def render_priority(
        self,
        data: bytes,
        *,
        content_type: str | None = None,
        flow: flow.Flow | None = None,
        http_message: http.Message | None = None,
        **unknown_metadata,
    ) -> float:
        if content_type and  content_type == "application/json":
            data_parsed = parse_json(data)
            if data_parsed is not PARSE_ERROR:
                #if "FileName" in data_parsed and "Content" in data_parsed:
                if "Content" in data_parsed:
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0


view = ASUView()



def load(loader: Loader):
    contentviews.add(view)

def done():
    contentviews.remove(view)
