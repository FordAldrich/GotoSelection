import os 
import sublime
import sublime_plugin

# This plugin will grab the current selection, or the word under the cursor, and automatically pre-fill the Goto Anything
# overlay with the given text.  For example, highlighting a class name and then invoking this plugin will open the 
# Goto Anything overlay and pre-fill it with the class name, which for my usage makes navigating my projects much easier.
# Default keybinding is ctrl + ;

class GotoSelectionCommand(sublime_plugin.WindowCommand):
    def run(self):
        # If you wish, you can enable the use of custom word separators.  Sublime Text will use these
        # to determine where a "word" begins and ends.  The values for these are set in the default settings,
        # or in the user settings if you've overridden them already.  Enabling this option will NOT
        # permanently change your settings.  It will save your current settings, change them temporarily,
        # and then write them back out.  Some may find it useful to change the word separator to be simply a space,
        # in which case this plugin will grab the current string until it reaches whitespace.  Note that enabling this 
        # option may lead to some extraneous output in your console as the settings file is saved .
        # (Sublime Text automatically re-parses the settings file if it detects that it has been modified.)
        #
        # To enable this functionality, change the value of 'overrideWordSeparators' to 'true'
        # If you wish to use a custom set of word separators, you may do so by editing the value of 
        # 'customWordSeparators' to reflect your needs.
        #
        # The characters that you wish to identify as a word separators should be entered inside the quotation marks, one 
        # after another, with nothing in between them.  Special characters must be escaped.  For example:
        #      customWordSeparators = ".;:/&#$"
        overrideWordSeparators = False
        customWordSeparators = " "

        # Get any active selections and iterate them
        for region in self.window.active_view().sel():
            if region.empty():
                # No active selection, so need to parse the word from the cursor position

                if overrideWordSeparators:
                    s = sublime.load_settings("Preferences.sublime-settings")
                    savedWordSeps = s.get("word_separators")
                    s.set("word_separators", customWordSeparators)

                    word = self.window.active_view().word(region)
                    lineContents = self.window.active_view().substr(word)

                    s.set("word_separators", savedWordSeps)
                else:
                    word = self.window.active_view().word(region)
                    lineContents = self.window.active_view().substr(word)
            else:
                # Selection exists, so simply retrieve it
                lineContents = self.window.active_view().substr(region)

        # Clean up any extra characters that don't need to be there - spaces, comments, etc.
        if len(lineContents) > 0:
            while (lineContents[0] in "# "):
                lineContents = lineContents[1:]

        # Call the goto overlay, give it the current word or selection, and ask it to show files
        self.window.run_command("show_overlay", {"overlay": "goto", "text": lineContents, "show_files": "true"})