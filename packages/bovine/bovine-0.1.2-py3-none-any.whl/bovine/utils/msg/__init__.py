from bovine import BovineClient
from bovine.clients import lookup_account_with_webfinger

from .validation import validate_tos


def validate(args):
    if not validate_tos(args.to):
        print("Invalid recipients")
        exit(1)

    if len(args.to) == 0 and not args.public:
        print("Specify at least one recipient")
        exit(1)


async def resolve(session, to):
    if "@" in to:
        return await lookup_account_with_webfinger(session, to)

    return to


async def process(args):
    async with BovineClient({"host": args.host, "private_key": args.secret}) as client:
        recipients = [await resolve(client.session, to) for to in args.to]

        mentions = [
            await client.object_factory.mention_for_actor_uri(recipient)
            for recipient in recipients
        ]
        mentions = [m.build() for m in mentions]

        note = client.object_factory.note(
            to=set(recipients), tag=mentions, content=args.message
        )

        if args.public:
            note = note.as_public()

        create = client.activity_factory.create(note.build()).build()

        await client.send_to_outbox(create)
