import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


from q2gui import q2style


class Q2Style(q2style.Q2Style):
    def _windows_style(self):
        focusable_controls_list = [
            "q2line",
            "q2check",
            "q2text",
            "q2button",
            "q2radio",
            "q2lookup",
            "q2combo",
            "q2toolbutton",
            "q2progressbar",
            "q2grid",
            "q2sheet",
            "q2date",
            "q2tab",
            "q2list",
            "q2spin",
            "q2doublespin",
            "QTabBar::tab",
            "QRadioButton",
            "#radio",
        ]
        focusable_controls = ", ".join(focusable_controls_list)
        focusable_controls_with_focus = ", ".join(["%s:focus" % x for x in focusable_controls_list])

        style = """
                QFrame,q2frame {{
                    background-color:{background};
                }}

                %(focusable_controls)s
                    {{
                        color:{color};
                        background-color:{background_control};
                        margin:{margin};
                        padding:{padding};
                        selection-color: {color_selection};
                        selection-background-color : {background_selection};
                    }}
                %(focusable_controls_with_focus)s
                    {{
                        background-color:{background_focus};
                        border: {border_focus};
                    }}
                QRadioButton:checked, QTabBar::tab:selected
                    {{
                        color: {color_selected_item};
                        background-color: {background_selected_item};
                        border: none;
                    }}
                QRadioButton:focus
                    {{
                        background-color: {background_focus};
                    }}

                q2spin {{border:{border};}}

                QTabBar::tab
                    {{
                        margin: {margin};
                        padding:0.1em 0.3em;
                    }}

                q2tab::pane{{
                    background:{background_selected_item};
                    border: {border};
                }}

                q2label{{
                    color:{color};
                    background: transparent;
                }}

                QGroupBox#title
                    {{
                        border: {border};
                        margin-top: 2ex;
                        padding: 2ex;
                    }}
                QGroupBox::title {{
                        subcontrol-origin: margin;
                        color: {color};
                        background-color:{background};
                        font: bold;
                        left: 1em;
                }}
                QMdiSubWindow, QMainWindow
                    {{
                        color: {color};
                        background-color: {background};
                    }}

                QMenuBar, QToolButton
                    {{
                        color: {color};
                        background-color: {background_control};
                    }}

                QMenuBar::item:selected
                    , QToolButton:hover
                    , QTabBar::tab:hover
                    , q2button:hover
                    , q2list::item:hover
                    , q2combo::item:selected
                    , QRadioButton:hover
                    {{
                        color: {color_selection};
                        background-color: {background_selection};
                    }}

                QToolButton
                {{
                    margin: 0px 0.1em;
                    padding-bottom: 0.1em;
                    border: 1px solid {color};
                }}


                QToolButton::menu-indicator
                    {{
                        subcontrol-origin: relative ;
                        bottom: -0.3em;
                    }}


                q2button
                    {{
                        border:{border};
                    }}

                q2space
                    {{
                        background:transparent;
                        border:none;
                    }}

                QToolBar {{background-color:transparent; padding: 0px; border:0px solid black;}}

                #main_tab_widget::tab-bar
                    {{
                        alignment: center;
                    }}

                #main_tab_bar::tab:last
                    {{
                        color:white;
                        max-height: 1ex;
                        width: 2em;
                        background:green;
                    }}
                #main_tab_bar::tab:last:hover
                    {{
                        color:green;
                        background:white;
                        max-height: 1ex;
                        width: 2em;
                        font: bold;
                    }}

                QSplitter:handle
                    {{
                        border-left: 0.1em dotted {color};
                        border-top: 0.1em dotted {color};
                    }}
                *:disabled {{color: {color_disabled};}}

                q2combo QAbstractItemView
                    {{
                        background:{background_focus};
                    }}
                QListView::item:selected
                    {{
                        background-color: {background_selection};
                        color: {color_selected_item};
                    }}

                QTableView
                    {{
                    alternate-background-color:{background};
                    }}

                QHeaderView::section, QTableView:focus
                    {{
                        color:{color};
                        background-color:{background_control};
                    }}

                QTableView:item::selected
                    {{
                        color: {color};
                        background-color:{background_focus};
                    }}

                QTableView QTableCornerButton::section,
                QTableWidget QTableCornerButton::section
                    {{
                        background-color:{background_control}; 
                        border:none;
                    }}

                #radio:focus
                    {{
                        background:{background_focus};
                    }}
            """ % locals()
        return style

    def _mac_style(self):
        return self._windows_style()

    def _linux_style(self):
        return self._windows_style()
