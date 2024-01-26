# This example requires the 'message_content' intent.
import discord
import os
import openai
from discord import app_commands, Interaction
from discord.ext import commands
from typing import Optional

MY_SECRET = os.getenv("SECRET_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

##### DATAS
details_parts = {
    0: {
        'Title': '\nPREAMBLE',
        'tags': '#preamble'
    },
    1: {
        'Title': 'PART I:\xa0THE UNION AND ITS TERRITORY',
        'tags': '#part-i-the-union-and-its-territory'
    },
    2: {
        'Title': 'PART II:\xa0CITIZENSHIP',
        'tags': '#part-ii-citizenship'
    },
    3: {
        'Title': 'PART III :\xa0FUNDAMENTAL RIGHTS',
        'tags': '#part-iii-fundamental-rights'
    },
    4: {
        'Title': 'PART IV: DIRECTIVE PRINCIPLES OF STATE POLICY',
        'tags': '#part-iv-directive-principles-of-state-policy'
    },
    25: {
        'Title': 'PART IVA: FUNDAMENTAL DUTIES',
        'tags': '#part-iva-fundamental-duties'
    },
    5: {
        'Title': 'PART V:\xa0THE UNION',
        'tags': '#part-v-the-union'
    },
    27: {
        'Title': 'CHAPTER I: THE EXECUTIVE',
        'tags': '#chapter-i-the-executive'
    },
    28: {
        'Title': 'CHAPTER II: PARLIAMENT',
        'tags': '#chapter-ii-parliament'
    },
    29: {
        'Title': 'CHAPTER III: LEGISLATIVE POWERS OF THE PRESIDENT',
        'tags': '#chapter-iii-legislative-powers-of-the-president'
    },
    30: {
        'Title': 'CHAPTER IV: THE UNION JUDICIARY',
        'tags': '#chapter-iv-the-union-judiciary'
    },
    31: {
        'Title': 'CHAPTER V: COMPTROLLER AND AUDITOR-GENERAL OF INDIA',
        'tags': '#chapter-v-comptroller-and-auditor-general-of-india'
    },
    6: {
        'Title': 'PART VI:\xa0THE STATES',
        'tags': '#part-vi-the-states'
    },
    23: {
        'Title': 'CHAPTER I: GENERAL',
        'tags': '#chapter-i-general'
    },
    24: {
        'Title': 'CHAPTER II: THE EXECUTIVE',
        'tags': '#chapter-ii-the-executive'
    },
    35: {
        'Title': 'CHAPTER III: THE STATE LEGISLATURE',
        'tags': '#chapter-iii-the-state-legislature'
    },
    36: {
        'Title': 'CHAPTER IV : LEGISLATIVE POWER OF THE GOVERNOR',
        'tags': '#chapter-iv-legislative-power-of-the-governor'
    },
    37: {
        'Title': 'CHAPTER V: THE HIGH COURTS IN THE STATES',
        'tags': '#chapter-v-the-high-courts-in-the-states'
    },
    38: {
        'Title': 'CHAPTER VI : SUBORDINATE COURTS',
        'tags': '#chapter-vi-subordinate-courts'
    },
    7: {
        'Title': 'PART VII: THE STATES IN PART B OF THE FIRST SCHEDULE',
        'tags': '#part-vii-the-states-in-part-b-of-the-first-schedule'
    },
    8: {
        'Title': 'PART VIII: THE UNION TERRITORIES',
        'tags': '#part-viii-the-union-territories'
    },
    9: {
        'Title': 'PART IX: THE PANCHAYATS',
        'tags': '#part-ix-the-panchayats'
    },
    40: {
        'Title': 'PART IXA: THE MUNICIPALITIES',
        'tags': '#part-ixa-the-municipalities'
    },
    41: {
        'Title': 'PART IXB: THE CO-OPERATIVE SOCIETIES',
        'tags': '#part-ixb-the-co-operative-societies'
    },
    10: {
        'Title': 'PART X: THE SCHEDULED AND TRIBAL AREAS',
        'tags': '#part-x-the-scheduled-and-tribal-areas'
    },
    11: {
        'Title': 'PART XI: RELATIONS BETWEEN THE UNION AND THE STATES',
        'tags': '#part-xi-relations-between-the-union-and-the-states'
    },
    42: {
        'Title': 'CHAPTER I: LEGISLATIVE RELATIONS',
        'tags': '#chapter-i-legislative-relations'
    },
    43: {
        'Title': 'CHAPTER II : ADMINISTRATIVE RELATIONS',
        'tags': '#chapter-ii-administrative-relations'
    },
    12: {
        'Title': 'PART XII: FINANCE, PROPERTY, CONTRACTS AND SUITS',
        'tags': '#part-xii-finance-property-contracts-and-suits'
    },
    44: {
        'Title': 'CHAPTER I: FINANCE',
        'tags': '#chapter-i-finance'
    },
    45: {
        'Title': 'CHAPTER II: BORROWING',
        'tags': '#chapter-ii-borrowing'
    },
    46: {
        'Title':
        'CHAPTER III: PROPERTY, CONTRACTS, RIGHTS, LIABILITIES, OBLIGATIONS AND SUITS',
        'tags':
        '#chapter-iii-property-contracts-rights-liabilities-obligations-and-suits'
    },
    47: {
        'Title': 'CHAPTER IV: RIGHT TO PROPERTY',
        'tags': '#chapter-iv-right-to-property'
    },
    13: {
        'Title':
        'PART XIII: TRADE, COMMERCE, AND INTERCOURSE WITHIN THE TERRITORY OF INDIA',
        'tags':
        '#part-xiii-trade-commerce-and-intercourse-within-the-territory-of-india'
    },
    14: {
        'Title': 'PART XIV: SERVICES UNDER THE UNION AND THE STATES',
        'tags': '#part-xiv-services-under-the-union-and-the-states'
    },
    48: {
        'Title': 'CHAPTER I: SERVICES',
        'tags': '#chapter-i-services'
    },
    49: {
        'Title': 'CHAPTER II: PUBLIC SERVICE COMMISSIONS',
        'tags': '#chapter-ii-public-service-commissions'
    },
    50: {
        'Title': 'PART XIVA:\xa0TRIBUNALS',
        'tags': '#part-xiva-tribunals'
    },
    15: {
        'Title': 'PART XV:\xa0ELECTIONS',
        'tags': '#part-xv-elections'
    },
    16: {
        'Title': 'PART XVI:\xa0SPECIAL PROVISIONS RELATING TO CERTAIN CLASSES',
        'tags': '#part-xvi-special-provisions-relating-to-certain-classes'
    },
    17: {
        'Title': 'PART XVII:\xa0OFFICIAL LANGUAGE',
        'tags': '#part-xvii-official-language'
    },
    51: {
        'Title': 'CHAPTER I: LANGUAGE OF THE UNION',
        'tags': '#chapter-i-language-of-the-union'
    },
    52: {
        'Title': 'CHAPTER II: REGIONAL LANGUAGES',
        'tags': '#chapter-ii-regional-languages'
    },
    53: {
        'Title':
        'CHAPTER III: LANGUAGE OF THE SUPREME COURT,\xa0HIGH COURTS, ETC.',
        'tags': '#chapter-iii-language-of-the-supreme-court-high-courts-etc'
    },
    54: {
        'Title': 'CHAPTER IV: SPECIAL DIRECTIVES',
        'tags': '#chapter-iv-special-directives'
    },
    18: {
        'Title': 'PART XVIII:\xa0EMERGENCY PROVISIONS',
        'tags': '#part-xviii-emergency-provisions'
    },
    19: {
        'Title': 'PART XIX:\xa0MISCELLANEOUS',
        'tags': '#part-xix-miscellaneous'
    },
    20: {
        'Title': 'PART XX:\xa0AMENDMENT OF THE CONSTITUTION',
        'tags': '#part-xx-amendment-of-the-constitution'
    },
    21: {
        'Title':
        'PART XXI:\xa0TEMPORARY, TRANSITIONAL AND\xa0SPECIAL PROVISIONS',
        'tags': '#part-xxi-temporary-transitional-and-special-provisions'
    },
    22: {
        'Title':
        'PART XXII:\xa0SHORT TITLE, COMMENCEMENT, AUTHORITATIVE TEXT\xa0IN HINDI AND REPEALS',
        'tags':
        '#part-xxii-short-title-commencement-authoritative-text-in-hindi-and-repeals'
    }
}
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@bot.event
async def on_ready():
  await bot.tree.sync()
  print("Bot is ready, ho gaya")


@bot.event
async def on_message(message):
  if message.author == bot.user or message.channel.id != 1200389727023546389:
    return
  else:
    await message.channel.send("Type /help to get more info of republic bot")


# @bot.tree.command()
# async def ping(interaction: Interaction):
#   await interaction.response.send_message("Pong!")


@bot.tree.command(name="help", description="get info about commands")
async def help(interaction: Interaction, parts: Optional[int] = None):
  allowed_channel_id = 1200389727023546389  # Replace with your desired channel ID
  if interaction.channel_id != allowed_channel_id:
    await interaction.response.send_message(
        "This command can only be used in the https://discord.com/channels/913712321161998348/1200389727023546389 channel."
    )
    return

  if parts is None:
    # Display general help
    await interaction.response.send_message(
        "## Constitution of India contains 395 articles in 22 parts. There are also 12 schedules in the Indian Constitution. If you are not aware about the parts in our constitution type /help <part number> and give any negative number or greater than 22, you will get a complete list of our constitution. Else you can type /help <part number> to get more info about the each part.\n\n"
    )

  elif parts >= 0 and parts < 23:
    info = details_parts[parts]["tags"]
    
    prompt = details_parts[parts]["Title"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "You are helpful assistant on Indian constitution"
        }, {
            "role":
            "user",
            "content":
            f"You are a wise person on Indian constituion. You have to give very concise response exact 2 sentence within 50 words(remember word count)\n{prompt}"
        }])

    extra=response["choices"][0]["message"]["content"]
    info2 = f"\nFor more details visit here https://www.clearias.com/constitution-of-india/{info}"
    ans = extra + info2
    await interaction.response.send_message(ans)
  else:
    message = ""
    for i in details_parts:
      details_parts[i]["Title"] = " -" + details_parts[i][
          "Title"] if "CHAPTER" in details_parts[i][
              "Title"] else details_parts[i]["Title"]
      message += details_parts[i]["Title"]
      message += "\n"
    message += "## :rocket: Now please let me know in which part you interested.\n"

    await interaction.response.send_message(
        "## You have entered invalid part number. Here is the list" + message)


bot.run(MY_SECRET)
