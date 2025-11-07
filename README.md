# LoreBroker Overview
LoreBroker is a simple offline program for managing AI RP lorebooks. It was designed specifically with Chub.ai 
in mind but lorebooks created here can also be exported to Silly Tavern.

## Installation
Both Windows and Linux are available on the [Releases](https://github.com/UlcyRegnum/lorebroker/releases) page. They should run with no addtional downloads.
I say should because most python installs will contain TKinter by default but if it doesn't you can install seperately.
You can also download the source directly and build yourself should that be something you're in to.

For Linux you'll need to make the file executable, 'chmod +x LoreBroker', first.

## FIELD EXPLANATION:
- Book Title: This is the title of the overall Lore Book. (Note: It does not pull into Chub. I'm not even sure if
    that's possible in chub, but works in ST.)
- Entry Title: This is the title of the individual Lore Book Entry and works in both Chub and ST.
- Keywords: These are the Keys that activate the content of the entry.
- Secondary Keywords: These are secondary keys that are active only when the Selective box is ticked.
- Selective: Determines iof secondary keys are used.
- Secondary Logic: Determines if secondary keys are inclusive (AND), or exclusive (NOT). (Note: In ST this is actually
    AND ANY and NOT ALL (Rather than Not Any)).
- Content: This is the content of the entry sent to the AI.
- Insertion Order: If multiple entries inserted, lower 'insertion order' = inserted higher.
- Constant: Whether to always trigger the entry (within the token budget).
- Probability: % chance of the content being activated when the entry is triggered. (Note: the exported JSON assumes
    this is turned ON because Chub doesn't have an on off, but ST does. Thusly, if left blank it will always
    default to 100)
- Priority: If token budget reached, lower priority value = discarded first.
- Case Sensitive: Whether the keywords are case-sensitive.
- Enabled: Whether this entry is enabled.
- Lore Entries: This is a scrolling list of entries that you've saved.

## USAGE Notes:
Import and Export JSON allow you to import and export JSON files. It works with both ST and Chub JSON formats. HOWEVER
because this program was designed with Chub in mind it lacks some fields that ST has. As a result some functions like
sticky, Cooldown, Delay, etc... Basically, anything not listed above in the Explanation section, are not contained in
the resulting export and ST will set them to the default values when you import to ST. Basically the same way any lore
entries would if you download a JSON from Chub and Import it to ST.

New Entry will clear the information currently in the form and generate a new blank entry. It would be wise to save the
entry you're working on before you add a new one. I may add a popup for this in the future.

Save Entry will save the current information into a new entry on the left under Lore Entries if none are selected, or
overwrite the currently selected one if one is selected. If no entry is selected on the left then it will also clear
the form. This was designed to help when creating a new Lore Book. It allows you to save an entry and
then immediately start the next one if you were starting a new book.

Delete Entry deletes the currently selected entry.

## IMPORTANT NOTES: I don't currently have any autosave implementation. You should save your lore books using Export JSON
regularly to avoid data loss. Please also keep a backup of your existing Lore Books if you're Importing them. While
I am pretty confident in what I've built it is always nice to have regular backups.

Please feel free to leave comments on Github :). I have tested this quite a bit, but I'm forever willing to admit that
I make mistakes. I'll try and get issues resolved as fast as I can. You're also welcome to leave PRs.
I can't promise I'll implement every one, but I'm happy to look into any request. Also, I'm aware my code is a mess,
that's next on my list.

Final note, this is my first real attempt at publishing something on Github. I admittedly have no idea what I'm doing.
Patience is appreciated :). - <3 Ulcy
