from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool(name="greet")
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run('stdio')