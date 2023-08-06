<p align="center"><img src="https://github.com/devliftz/lift.bot/blob/main/img/lift.bot.png?raw=true" width=200px" alt="project-image"></p>

<h1 align="center" id="title">lift.bot</h1>


<p id="description">Best discord.py customized library. With easier usage less time to spend on reading docs and mobile status built in.</p>

<p align="center"><img src="https://img.shields.io/discord/1065186413865357343?color=5865F2&amp;label=Discord&amp;logo=discord&amp;logoColor=white&amp;style=for-the-badge" alt="shields">
<img src="https://img.shields.io/youtube/channel/subscribers/UCty3ao3DSrd7_qxAiRbCGEg?color=red&amp;label=Youtube&amp;logo=youtube&amp;style=for-the-badge" alt="shields">
<img src="https://img.shields.io/github/downloads/devliftz/lift.bot/total?color=000000&amp;label=downloads&amp;logo=github&amp;logoColor=white&amp;style=for-the-badge" alt="shields"></p>

<h2>Project Screenshots:</h2>
<h2 style="color: 000000;"></h2>

#### Console Formatting

<img src="https://github.com/devliftz/lift.bot/blob/main/img/prev.png?raw=true" alt="project-screenshot" width="400" height="400/">

<h2>Installation Guide</h2>

- Install lift.bot library `pip install lift.bot`
- Create `main.py`

<h2>Examples</h2>

```py
from lift import lft

# Example command
@lft.bot.command()
async def hi(ctx):
    await ctx.reply(f"Hey, {ctx.author.name}")

lft.login("token")
```