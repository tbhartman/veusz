#    Copyright (C) 2005 Jeremy S. Sanders
#    Email: Jeremy Sanders <jeremy@jeremysanders.net>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

# $Id$

"""Module for creating QWidgets for the settings, to enable their values
   to be changed.
"""

import qt
import setting

class SettingEdit(qt.QLineEdit):
    """Main control for editing settings which are text."""

    def __init__(self, setting, parent):
        """Initialise the setting widget."""

        qt.QLineEdit.__init__(self, parent)
        self.setting = setting
        self.bgcolour = self.paletteBackgroundColor()

        # set the text of the widget to the 
        self.setText( setting.toText() )

        self.connect(self, qt.SIGNAL('returnPressed()'),
                     self.validateAndSet)
        self.connect(self, qt.SIGNAL('lostFocus()'),
                     self.validateAndSet)

        # set tooltip for description
        d = setting.getDescription()
        if d != '':
            qt.QToolTip.add(self, d)
        
    def validateAndSet(self):
        """Check the text is a valid setting and update it."""

        text = str(self.text())
        try:
            val = self.setting.fromText(text)
            self.setPaletteBackgroundColor(self.bgcolour)
            
            # value has changed
            if self.setting.get() != val:
                self.setting.set(val)
                self.emit( qt.PYSIGNAL('settingValueChanged'), () )

        except setting.InvalidType:
            self.setPaletteBackgroundColor(qt.QColor('red'))

class BoolSettingEdit(qt.QCheckBox):
    """A check box for changing a bool setting."""
    
    def __init__(self, setting, parent):
        qt.QCheckBox.__init__(self, parent)

        self.setting = setting
        self.setChecked( setting.get() )

        # we get a signal when the button is toggled
        self.connect( self, qt.SIGNAL('toggled(bool)'),
                      self.slotToggled )

        # set tooltip for description
        d = setting.getDescription()
        if d != '':
            qt.QToolTip.add(self, d)

    def slotToggled(self, state):
        """Emitted when checkbox toggled."""

        self.setting.set(state)
        self.emit( qt.PYSIGNAL('settingValueChanged'), () )
        
# class SettingEditAuto(qt.QComboBox):
#     """For editing settings which allow auto values."""

#     def __init__(self, setting, *args):
#         qt.QComboBox.__init__(self, *args)
#         self.setting = setting
#         self.bgcolour = self.paletteBackgroundColor()

#         # we want the user to be able to edit items
#         self.setEditable(True)

#         # makes it obvious it can be auto
#         self.insertItem('Auto')

#         # set the text of the widget to the 
#         self.setCurrentText( setting.toText() )

#         # set tooltip for description
#         d = setting.getDescription()
#         if d != '':
#             qt.QToolTip.add(self, d)

#     def focusOutEvent(self, *args):
#         """Allows us to check the contents of the widget."""
        
#         qt.QComboBox.focusOutEvent(self, *args)
#         self.validateAndSet()
        
#     def validateAndSet(self):
#         """Check the text is a valid setting and update it."""

#         text = str(self.currentText())
#         try:
#             val = self.setting.fromText(text)
#             self.setPaletteBackgroundColor(self.bgcolour)
            
#             # value has changed
#             if self.setting.get() != val:
#                 self.setting.set(val)
#                 self.emit( qt.PYSIGNAL('settingValueChanged'), () )

#         except setting.InvalidType:
#             self.setPaletteBackgroundColor(qt.QColor('red'))

class SettingChoice(qt.QComboBox):
    """For choosing between a set of values."""

    def __init__(self, setting, iseditable, vallist, parent):
        qt.QComboBox.__init__(self, parent)
        self.setting = setting
        self.bgcolour = self.paletteBackgroundColor()

        self.setEditable(iseditable)

        # add items to list
        items = qt.QStringList()
        for i in vallist:
            items.append(i)
        self.insertStringList(items)

        # set the text of the widget to the 
        self.setCurrentText( setting.toText() )

        # set tooltip for description
        d = setting.getDescription()
        if d != '':
            qt.QToolTip.add(self, d)

        # if a different item is selected
        self.connect( self, qt.SIGNAL('activated(const QString&)'),
                      self.slotActivated )

    def focusOutEvent(self, *args):
        """Allows us to check the contents of the widget."""
        
        qt.QComboBox.focusOutEvent(self, *args)
        self.slotActivated('')

    def slotActivated(self, val):
        """If a different item is chosen."""

        text = str(self.currentText())
        try:
            val = self.setting.fromText(text)
            self.setPaletteBackgroundColor(self.bgcolour)
            
            # value has changed
            if self.setting.get() != val:
                self.setting.set(val)
                self.emit( qt.PYSIGNAL('settingValueChanged'), () )

        except setting.InvalidType:
            self.setPaletteBackgroundColor(qt.QColor('red'))