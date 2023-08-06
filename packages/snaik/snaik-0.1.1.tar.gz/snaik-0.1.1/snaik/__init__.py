import pyqtgraph as pg
from packaging.version import Version

if Version(pg.__version__) <= Version("0.13.3"):
    from pyqtgraph.parametertree.parameterTypes.basetypes import GroupParameterItem

    # Monkeypatch pyqtgraph's parameter item to look OK on dark mode if required
    def updateDepth(self, depth):
        """
        Change set the item font to bold and increase the font size on outermost groups.
        """
        for c in [0, 1]:
            font = self.font(c)
            font.setBold(True)
            if depth == 0:
                font.setPointSize(self.pointSize() + 1)
            self.setFont(c, font)
        self.titleChanged()

    GroupParameterItem.updateDepth = updateDepth

__version__ = "0.1.1"
from snaik.game import Game
from snaik.window import SnaikWindow
