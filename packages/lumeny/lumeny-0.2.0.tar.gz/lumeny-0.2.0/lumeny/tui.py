from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from MinifluxConnector import connect_miniflux 

# create a widget to display all starred feed titles
class FeedPreview(Static):
    """A widget to display a feed 

    Args:
        App (_type_): _description_

    Returns:
        _type_: _description_
    """


# create a widget to display feed content

class LumenApp(App):
    """A textual app to display miniflux starred entries""" 
    
    # bind key q to quit, j to move down, k to move up, l to display feed content
    BINDINGS = { "q": "quit", "j": "down", "k": "up", "l": "display_feed_content" }
    
    def compose(self) -> ComposeResult:
        """Compose the UI"""
        # create a header widget
        header = Header("Lumen")
        # create a footer widget
        footer = Footer("Press q to quit")
        # create a list widget
        list = self.view.list(
            name="list",
            items=["Item 1", "Item 2", "Item 3"],
            on_select=self.on_select,
        )
        # return the widgets
        return ComposeResult(
            content=header + list + footer,
            status=footer,
            focus=list,
        )
    
    def move_down(self) -> None:
        """Move the focus down"""
        self.view.move_focus("down")
    
    def move_up(self) -> None:
        """Move the focus up"""
        self.view.move_focus("up")
    
    def action_quit(self) -> None:
        """Quit the app"""
        self.stop()
    
    def display_feed_content(self) -> None:
        """Display the feed content"""
        # get the current selected item
        item = self.view.get("list").selected
        # display the item
        self.log(f"You selected {item}")
        

if __name__ == "__main__":
    LumenApp.run(log="textual.log")
    
