#!/usr/bin/env python
# coding: utf8

import sublime_plugin
import sublime


class AutoIndent(sublime_plugin.EventListener):
    def on_load(self, view):
        def get_indent(content):
            lines = content.split('\n')
            commented = False
            leading_tab = False
            leading_space = False
            leading_spaces = 0

            for line in lines:
                stripped = line.strip()

                # blank line
                if stripped.__len__() == 0:
                    continue

                # commented block
                if commented:
                    if stripped.find('*/') != -1:
                        commented = False
                    continue
                elif stripped.find('/*') == 0:
                    commented = True
                    continue
                elif stripped.find('/*') != -1:
                    commented = True

                # commented line
                if stripped.find('//') == 0 or stripped.find('#') == 0 or stripped.find('%') == 0:
                    continue

                leading_char = line[0:1]

                # tab is the leading character
                if leading_char == '\t':
                    leading_tab = True
                elif leading_char == ' ':
                    if leading_space == False or leading_spaces > line.find(stripped):
                        leading_spaces = line.find(stripped)
                    leading_space = True

            return leading_tab, leading_space, leading_spaces

        content = view.substr(sublime.Region(0, view.size()))

        leading_tab, leading_space, leading_spaces = get_indent(content)

        s = view.settings()

        # only tabs
        if leading_tab and not leading_space:
            s.set('translate_tabs_to_spaces', False)
        # only spaces
        elif leading_space and not leading_tab:
            s.set('translate_tabs_to_spaces', True)
            s.set('tab_size', leading_spaces)
        # both tabs and spaces
        elif leading_space and leading_tab:
            s.set('translate_tabs_to_spaces', False)
            if leading_spaces != 0:
                s.set('tab_size', leading_spaces)
