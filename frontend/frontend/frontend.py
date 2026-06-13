import reflex as rx
import requests

class State(rx.State):
    """The app state."""
    url: str = ""
    markdown_output: str = ""
    is_loading: bool = False
    error_message: str = ""

    def update_url(self, value: str):
        self.url = value

    def generate_readme(self):
        """Calls your FastAPI backend to generate the README."""
        if not self.url or "github.com" not in self.url:
            self.error_message = "Please enter a valid GitHub URL."
            return
            
        # Reset state and show loading spinner
        self.is_loading = True
        self.error_message = ""
        self.markdown_output = ""
        yield  # Yield updates the UI immediately
        
        try:
            # Call the backend we built
            response = requests.post(
                "https://readme-agent-g5or.onrender.com/api/generate",
                json={"url": self.url}
            )

            if response.status_code != 200:
                error_detail = response.json().get("detail", "Unknown backend error")
                self.error_message = f"API Error: {error_detail}"
                return
            
            response.raise_for_status()
            
            # Save the result
            self.markdown_output = response.json().get("markdown", "")
        except Exception as e:
            self.error_message = f"Error generating README: Ensure backend is running. ({str(e)})"
        finally:
            self.is_loading = False
            yield 

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            
            # Header
            rx.heading("README Generator", 
                       size="9",
                    #    background_image="linear-gradient(to right, #F2EB83, #83DCF2, #A183F2, #F283A4)", # Tailwind equivalent of from-indigo-600 to-purple-600
                    # background_clip="text",
                        # color="transparent",
                       ),
            rx.text("Paste a GitHub repository URL to generate a comprehensive README.md using AI.", 
                    color="gray",
                    # high_contrast=True
                    ),
            
            # Input and Button
            rx.hstack(
                rx.input(
                    placeholder="https://github.com/owner/repo",
                    on_change=State.update_url,  # <--- UPDATE THIS LINE
                    width="400px"
                ),
                rx.button(
                    "Generate",
                    background_image="linear-gradient(to right, #DE2810)",
                    on_click=State.generate_readme,
                    loading=State.is_loading,
                    width="120px"
                ),
                width="100%",
                justify="center",
                margin_top="4"
            ),
            
            # Error Message
            rx.cond(
                State.error_message != "",
                rx.callout(State.error_message, icon="alert_triangle", color_scheme="red", margin_top="4"),
            ),
            
            # Output Box (Only shows if markdown_output is not empty)
            rx.cond(
                State.markdown_output != "",
                rx.box(
                    rx.hstack(
                        rx.heading("Preview", size="5"),
                        rx.spacer(),
                        # The Magic Copy Button
                        rx.button(
                            rx.icon(tag="copy"),
                            "Copy Markdown",
                            on_click=rx.set_clipboard(State.markdown_output),
                            variant="soft",
                            cursor="pointer"
                        ),
                        width="100%",
                        padding_bottom="4"
                    ),
                    # The Markdown Preview
                    rx.box(
                        rx.markdown(State.markdown_output),
                        padding="6",
                        border="1px solid #eaeaea",
                        border_radius="8px",
                        width="100%",
                        background_color="#02011C",
                        color="white"
                    ),
                    width="100%",
                    margin_top="8"
                )
            ),
            
            align="center",
            spacing="6",
            padding="10",
            width="100%",
            max_width="800px"
        ),

        background_image="linear-gradient(to bottom, #010005, #010005, #043D07, #CEF28F)",
        width="100%",
        min_height="100vh"
    )

app = rx.App()
app.add_page(index)