import os
import aiohttp
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


@client.tree.command(name="pr0gramm", description="Postet das neueste Top-Bild von pr0gramm.com")
async def pr0gramm(interaction: discord.Interaction):
    """Fetch and post the latest top item from pr0gramm.com"""
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

    # Skip pinned items (mark=14 is the pr0gramm pinned marker, or promoted is very large)
    item = None
    for candidate in items:
        if not candidate.get("pinned", False):
            item = candidate
            break

    if item is None:
        item = items[0]  # fallback: just take the first

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
