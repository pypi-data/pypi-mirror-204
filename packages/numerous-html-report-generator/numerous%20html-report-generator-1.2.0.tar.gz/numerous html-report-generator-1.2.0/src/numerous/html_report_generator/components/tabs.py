from itertools import count
from numerous.html_report_generator.block import Block


class Tabs(Block):
    """
    Attributes:
        id (int): Unique id for each tabs object
        tabs (dict): Content of tabs. Each key will be used as name of the buttons.
            The values of the dict will be used as html content in the tab.
    """

    _ids = count(0)
    _unique_tab_id = count(0)

    def __init__(self):

        self.id = next(self._ids)
        self.tabs = {}

    def set_tabs(self, tabs):
        self.check_tabs(tabs)
        self.tabs = tabs

    def add_tabs(self, tabs):
        self.check_tabs(tabs)
        self.tabs.update(tabs)

    def check_tabs(self, tabs):
        assert type(tabs) == dict


    def _as_html(self):

        tab_script = """\n\n<script>
                function openTab_""" + str(self.id) + """(evt, tabname) {
                  var i, tabcontent, tablinks;
                  tabcontent = document.getElementById('""" + str(self.id) + """').getElementsByClassName("tabcontent");

                  for (i = 0; i < tabcontent.length; i++) {

                    tabcontent[i].style.display = "none";
                  }

                  tablinks = document.getElementById('""" + str(self.id) + """').getElementsByClassName("tablinks");
                  for (i = 0; i < tablinks.length; i++) {
                    tablinks[i].className = tablinks[i].className.replace(" active", "");
                  }
                  thistab = document.getElementById(tabname);
                  //thistab.style.width= '100%';
                  thistab.style.display = "block";
                  //window.dispatchEvent(new Event('resize'));
                  evt.currentTarget.className += " active";
                }
                var evt = document.createEvent("MouseEvents");
                evt.initMouseEvent("click", true, true, window, 1, 0, 0, 0, 0,
                    false, false, false, false, 0, null);

                document.getElementById('default_tab_""" + str(self.id) + """').dispatchEvent(evt);
                </script>\n\n"""
        tab_divs = []
        tab_buttons = []

        for label, content in self.tabs.items():

            unique_tab_id = next(self._unique_tab_id)

            tab_label = f"""
            <button 
                id=default_tab_{self.id} 
                class="tablinks" 
                onclick="openTab_{self.id}(event, 'tab_{unique_tab_id}')">{label}
            </button>"""

            tab_div = f"""
            <div id="tab_{unique_tab_id}" class="tabcontent" style="display: block;" width="100%">
                  {content}
            </div>"""



            tab_divs.append(tab_div)
            tab_buttons.append(tab_label)



        buttons = "".join(tab_buttons)
        tabs = "".join(tab_divs)
        html = f'<div id="{self.id}"><div class="tab">{buttons}</div>{tabs}</div>{tab_script}'

        return html
