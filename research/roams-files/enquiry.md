
# Let's find the limits of the Roam json import! #

## UIDs ##

I tried to export some file and then import it again. Got the error

``` 
Import failed: blocks already exist
```

So the blocks are probably unique. I assume that Roam tells them apart with individual uid's.

But I can import files where the blocks don't have UIDs, roam just then adds them then.

## Numbered lists ##

Removing the UIDSs from an example file with numbered lists yields a Roam document without numbered lists. This means that Roam somehow remembers which individual blocks are numbered. Since this information is not stored in the json-file itself there is probably no way to keep that part of the structure of the Markdown file when converting it to a Roam document.

## What can we leave out ##

We've already figured out that we can leave out the UIDs. As it turns out we can also drop `create-email`, `create-time`, `edit-email` and `edit-time`. Roam will add them automatically.

## What we need to put in

So for a simple text structure like this:

- Document Title
    + Some bullet point
    + Some other bullet point
        * Some further nested bullet point

we are left with a Roam json structure like this:

```json
[
   {
      "title":"Document Title",
      "children":[
         {
            "string":"Some bullet point"
         },
         {
            "string":"Some other bullet point",
            "children":[
            {
                "string":"Some further nested bullet point"
            }
            ]
         }
      ]
   }
]
```

## Headings, bold, italics #

Headings are represented with the json property `"heading"` and a corresponding integer.

__Bold__ text is represented by `**double asterisks**`.

_Italics_ are represented by `__double underscores__`.

