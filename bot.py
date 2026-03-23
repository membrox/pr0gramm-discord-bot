import os
import aiohttp
import random
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# pr0gramm image base URL
IMG_BASE = "https://img.pr0gramm.com/"
POST_BASE = "https://pr0gramm.com/top/"

# flags=1 = SFW only. Use flags=7 for all content (SFW + NSFW + NSFL)
PR0GRAMM_API = "https://pr0gramm.com/api/items/get?promoted=1&flags=1"


class Pr0Bot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()
        print("Slash commands synced.")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="pr0gramm.com/top",
            )
        )


client = Pr0Bot()


@client.tree.command(name="pr0gramm", description="Postet ein Top-Bild von pr0gramm.com")
@app_commands.describe(is_random="Wählt einen zufälligen Post aus der Top-Liste (statt dem neuesten)")
@app_commands.rename(is_random="random")
async def pr0gramm(interaction: discord.Interaction, is_random: bool = False):
    """Fetch and post a top item from pr0gramm.com"""
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                PR0GRAMM_API,
                headers={"User-Agent": "pr0gramm-discord-bot/1.0"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status != 200:
                    await interaction.followup.send(
                        f"❌ pr0gramm API antwortete mit Status {resp.status}."
                    )
                    return
                data = await resp.json()
    except Exception as e:
        await interaction.followup.send(f"❌ Fehler beim Abrufen der pr0gramm-API: `{e}`")
        return

    items = data.get("items", [])
    if not items:
        await interaction.followup.send("❌ Keine Einträge von pr0gramm gefunden.")
        return

    # Filter out pinned items
    candidates = [i for i in items if not i.get("pinned", False)]
    if not candidates:
        candidates = items  # fallback if all are pinned

    if is_random:
        item = random.choice(candidates)
    else:
        item = candidates[0]

    image_path = item["image"]
    item_id = item["id"]
    username = item.get("user", "?")
    upvotes = item.get("up", 0)
    downvotes = item.get("down", 0)
    post_url = f"{POST_BASE}{item_id}"
    img_url = IMG_BASE + image_path

    # Determine if it's a video or image
    is_video = image_path.endswith(".mp4") or image_path.endswith(".webm")

    embed = discord.Embed(
        title=f"🔥 Top von pr0gramm – von **{username}**",
        url=post_url,
        color=discord.Color.from_rgb(238, 102, 34),  # pr0gramm orange
    )
    embed.set_footer(text=f"👍 {upvotes}  👎 {downvotes}  •  pr0gramm.com/top/{item_id}")

    if is_video:
        # Discord can't embed video in an embed, so we send the URL directly
        embed.description = f"🎬 **Video-Post** – [Direkt ansehen]({img_url})\n\n[Zum Post]({post_url})"
        # Use thumbnail from the thumb field if available
        thumb_path = item.get("thumb", "")
        if thumb_path:
            embed.set_image(url=IMG_BASE + thumb_path)
        await interaction.followup.send(content=img_url, embed=embed)
    else:
        embed.set_image(url=img_url)
        await interaction.followup.send(embed=embed)


def main():
    if not TOKEN:
        print("❌ DISCORD_TOKEN fehlt! Bitte .env Datei anlegen (siehe .env.example).")
        return
    client.run(TOKEN)


if __name__ == "__main__":
    main()
