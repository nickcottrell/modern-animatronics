# Modern Animatronics

*Notes from a small, questionably managed attraction in Ladera Ranch, California.*

Some of my family still think we moved to Los Angeles.

We live in Ladera Ranch, which is far enough away for that to be geographically misleading, but I understand how the confusion persists. Every so often I send them photographs of an elaborate theatrical attraction outside our house. This does very little to establish that we lead a normal life.

Inside, we have homework, laundry, and the usual administrative problems of being a family. Outside, a seven-foot ship captain guards a glowing chest of cursed treasure.

The bird next to him has its own sound system.

I should probably explain.

***

Every Halloween, I pay homage to the original Pirates of the Caribbean ride outside our house. There are skeletons, foliage, fog machines, lighting effects, a talking pirate, a talking bird, a treasure chest, and an increasingly unreasonable amount of supporting infrastructure.

Usually, it spreads onto the lawn. This year, rain forced the production onto the porch.

This required some compromises in the geographical scale of the pirate world. The captain was now operating considerably closer to the welcome mat.

But I liked the compression. Everything was within reach. I could see how the pieces fit together. What had previously been a yard full of equipment became a small stage.

The weather reduced the size of the attraction and improved my access to its machinery. I counted this as a design feature. On Halloween night, I am also the attraction’s primary and only ride operator, technician, and cast member.

***

The treasure chest requires the most supervision.

There is no candy in it. It contains fake treasure, artifacts, and a skull, arranged and hot-glued into a composition suggesting several poor decisions were made during an expedition.

A green light illuminates it from inside. Fog arrives through a pipe connected to a modified cooler. In the dark, the chest appears to contain something you should probably leave alone.

Naturally, children want to look inside.

This is one of the satisfying things about building a scene. You arrange some objects, give them light and atmosphere, and people begin supplying the story. A skull sitting on a table is a decoration. A skull half-visible inside a glowing, smoking treasure chest raises questions.

I don’t need to answer most of them. I need to keep the fog cold.

That turns out to be an actual job.

The cooler contains ice that chills the fog before it enters the chest. When the effect is working, the fog spills over the edges and settles in a way that feels appropriately supernatural. As the ice melts, its behavior changes. Eventually, the chest just spews stage fog onto the porch, making it look more like a heavy metal show.

The machine works. The scene is breaking down.

The ice is a consumable, which means the atmosphere has an operating budget and a maintenance schedule.

***

Inside, we are watching a movie.

This year, Kim and I dressed as Dr. Ellie Sattler and Dr. Alan Grant from *Jurassic Park*.

People might reasonably ask why I don’t dress as a pirate, given the substantial investment in pirate infrastructure.

I used to. But a wig and captain’s hat become less charming when you are carrying buckets of ice, bending over extension cords, and trying to find where you put the candy.

Alan Grant has practical clothes. He looks like someone who could address an equipment problem.

So we put on *Jurassic Park* while the pirate attraction operated outside. I periodically emerged to distribute candy, help small children negotiate the situation, and inspect the atmospheric conditions around the cursed treasure.

Being dressed as a helpful paleontologist also made it easier to reassure anyone who wasn’t quite ready to approach a seven-foot pirate.

Inside, John Hammond, the delighted founder of a theme park populated with living dinosaurs, was showing off his investment.

“Spared no expense.”

I understood the enthusiasm. There is something reassuring about watching a film in which the people responsible for an attraction have made significantly worse operational decisions than I have.

At least mine doesn’t breed.

Meanwhile, in the control room, Samuel L. Jackson, playing the park’s chief engineer, starts the automated tour.

“Hold onto your butts.”

I appreciate an engineer who communicates uncertainty clearly.

***

Outside, the lights were coming into their own. Families were approaching, and I still had an optimistic relationship with my ice supply. Anyone coming through the rain deserved a substantial handful of candy.

Each trip through the front door interrupted one attraction with the demands of another.

A photograph. More candy. A small child considering whether the captain could be trusted. A quick inspection of the chest.

Back inside, the tour vehicles were stopped beside the Tyrannosaurus enclosure in a tropical storm. The electric fence had lost power. A glass of water began to tremble.

I had missed some developments.

This is one disadvantage of operating an attraction while watching *Jurassic Park*. You return to discover that several of your management assumptions are being examined at considerable volume.

I went back out to check the fog.

***

The bird, meanwhile, has no responsibilities.

It sits beside its own speaker, delivering prerecorded remarks from a small USB stick on an independent loop. The main soundtrack plays separately: an edited sequence following the original Pirates of the Caribbean ride audio, giving the scene a longer, roughly twenty-minute cycle.

That soundtrack reaches an ordinary boombox through a short-range FM transmitter in the garage. I like using equipment I’m willing to leave outside, and there is something pleasing about tuning a radio to receive your own little pirate world.

The two don’t need to agree about exactly where they are.

The bird can say its thing while the music moves through another section. The lights continue. The fog drifts. Someone leans toward the chest.

The captain has a third arrangement: a motion sensor starts his own sequence of speech and movement when someone approaches.

Together, these separate activities make the whole thing feel like a place.

***

That interests me because much of my software work concerns relationships between independently operating parts. What context does each part need? What can it do by itself? When does it need a signal from somewhere else?

Here, I can walk around those questions and follow their extension cords.

The bird doesn’t know whether the fog is working.

The fog machine doesn’t know whether anyone is there. The captain can detect an approaching visitor, but this gives him no particular insight into the condition of his treasure.

I maintain that part of the picture.

The ice melts. The fog changes. Something that looked right a few minutes ago needs attention. Meanwhile, the bird carries on, the soundtrack continues, and the captain addresses whoever has activated him.

There is something useful about their independence. Replenishing the cooler doesn’t require suspending maritime operations. Each component contributes what it can while I attend to another part of the scene.

Coordination is largely a service I provide.

I know how the whole thing is supposed to feel. I watch it, notice what has changed, and intervene. There is no message from the cooler announcing that its contribution to the illusion has deteriorated.

I have to go look.

Perhaps an unreasonable amount of distributed-systems thinking to apply to a treasure chest.

It is also what happens when you give me a treasure chest.

***

Now I’m wondering what else the radio signal could carry.

Could I put the soundtrack on the left channel and control cues on the right? With a receiver that could separate and interpret them, could a cue start a short sequence of sound, light, and movement?

The captain already responds to motion. What interests me is giving that response a little company. A change in the lighting. A sound from somewhere else. A brief suggestion that the inhabitants of the porch are involved in the same incident.

Then the scene could settle back into its independent loops.

MIDI is another possibility. Small modules, recognizable cues, sequences that can run locally and occasionally come together.

I haven’t built that part yet. Maybe next year.

Moving everything onto the porch has made it dangerously easy to consider. I can reach the equipment. I can follow the wires. I can change something and see what happens without walking across the lawn.

For now, I replace the ice.

***

But I keep thinking about the difference between sending a command to start something and sending a description of how it should unfold.

A trigger gives you an event: move now.

A control curve gives you a shape over time. Turn slowly. Pause. Return quickly. With an appropriate encoding and a controller that understands it, those changing values can travel through an audio channel and emerge as a physical gesture.

A head that turns steadily feels different from one that hesitates, accelerates, and settles into position. Somewhere in those differences, the captain acquires an attitude.

***

I’m listening to James Gleick’s *Chaos* while putting this together, which is doing very little to contain the scope of the project.

Gleick is a science writer tracing how researchers began to understand systems whose behavior could be intricate and difficult to predict even when the underlying rules were simple. Weather. Turbulence. Populations rising and falling. One way to study such behavior is to represent a system’s changing condition as a path through a space of possible states.

That way of looking at things has lodged in my head.

Imagine plotting the captain’s head angle against the brightness of the light inside the chest. At any instant, that pair of values gives you a point. As the head turns and the light changes, the point traces a path.

Those two measurements would describe only a small part of the scene. But I could already imagine different paths producing different impressions: a slow look toward a gradually brightening chest, or a sudden turn as the light drops.

The movement doesn’t have to be chaotic for the picture to be useful.

I started by wondering how to make the pirate move. Now I’m considering the shape of his attention.

At my computer, I work on other kinds of coordinates.

***

This is also where the nostalgia turns out to contain a technical specification.

Disney’s Enchanted Tiki Room opened in 1963. Its birds, flowers, and other inhabitants performed with the help of multichannel magnetic tape. Recorded control signals coordinated their movements alongside the music, dialogue, and effects.

Audio-Animatronics.

The “audio” was doing more than providing something to sing along to. The recording carried signals that machinery could interpret as actions. A mouth opened. A head turned. Several figures participated in the same musical incident.

The performance had a control system running through it.

Walt himself described the equipment in the language of Space Age guidance systems. I like that the machinery of the future was being recruited to operate a room full of singing birds.

I would like to recruit some of it for the porch.

But following that thought means going a little further backstage. Before anyone could put a convincing performance on tape, there were questions about what a signal could carry, how reliably it could arrive, and what the receiving mechanism would do with it.

Then there was the question I kept encountering at the cooler.

How do you know whether the thing you told the machine to do actually worked?

***

Two people worth meeting here are Claude Shannon and Norbert Wiener.

Shannon was a mathematician at Bell Labs. In 1948, he published a theory of how information could be measured, encoded, and transmitted reliably through imperfect channels. His work helped establish the foundations of digital communication. A phone call, a text message, a picture arriving intact on another screen: these are everyday encounters with problems he helped make mathematically tractable.

That same year, Wiener, a mathematician at MIT, published *Cybernetics*, connecting communication and control through feedback in machines and living things.

*Cybernetics* is an excellent word to encounter while considering modifications to a seven-foot pirate. It suggests that the next reasonable purchase might be a mechanical arm.

But you can begin with a thermostat. It measures the temperature, compares it with a setting, and uses the difference to govern the heating. What happens in the room affects what the system does next.

On the porch, I could send a perfectly good command to the fog machine and still get disappointing fog.

The message arrived. The ice melted.

Those are different problems.

Shannon helps me think about getting an instruction through. Wiener helps me think about what happens when information about the result comes back.

***

At present, that information comes back when I open the front door.

On a rainy Halloween evening, this also gives me an opportunity to discover whether anyone has braved the weather. Anyone who has gets a handful of candy while I inspect the atmospheric conditions.

The feedback mechanism has several duties.

The thermostat has a setting. My porch has an opinion.

I can tell when the fog looks right, but explaining what “right” means takes a little more work. It should spill from the chest and linger around the treasure. Enough to suggest something troubling happened on that expedition. The skull should remain partly visible.

If I wanted a machine to manage this, what would I ask it to measure?

The temperature inside the cooler would tell me something. So would the amount of ice remaining. Neither would tell me exactly what a child approaching from the sidewalk could see.

For now, I can walk over and look. I inspect the result, compare it with the unreasonable picture in my head, and replace the ice.

I have built a control loop with a dad in it.

The arrangement works. But every proposed improvement requires me to make another piece of that picture explicit: what matters, what can vary, and what would count as a useful correction.

I went outside to maintain the atmosphere.

Now I’m trying to specify it.

***

The attraction already works. People stop, look, take photographs. Occasionally, someone very small decides the captain is too much pirate, and Alan Grant assists with negotiations.

My dissatisfaction is more specialized.

I can imagine the whole scene changing character for a while. The lights shift. The soundtrack builds. A few movements land together, and suddenly there’s a pirate battle underway. Then the excitement subsides into something quieter: water, insects, a low-lit chest, the suggestion of a bayou with unresolved historical problems.

The bird continues to offer its perspective.

I want those larger changes to pass through the scene like waves. Each component could participate in a short sequence, then return to its usual activity. Another sequence could begin while the rest of the world keeps running.

That leaves some decisions to make.

What does each component need to receive? A command for every movement? A cue to begin a sequence it already knows? Some description of the current mood, with rules for how it should contribute?

And if it misses the message, could it catch enough of the next one to join in?

I’m standing beside a treasure chest considering how a pirate might acquire context incrementally.

***

This is familiar territory. I’ve been working on another way for a receiver to watch a repeating sequence and gradually assemble something useful.

In my software work, I’ve been building components for an optical transfer protocol. The basic idea is to let a camera collect a message from a sequence of QR codes.

A single QR code gives you one frame to scan. A repeating sequence lets you divide a larger message into pieces and distribute them over time.

Hold up your phone. It starts collecting.

You don’t have to catch the beginning. If the camera misses a piece, it gets another opportunity when that piece returns. The receiver keeps track of what it has until it has enough to reconstruct the message.

Then the arrangement becomes interesting.

Which pieces should repeat most often? What belongs between them? How much can the camera reliably read before the image changes? I can interleave different parts and give some more frequent appearances, composing a sequence around what the receiver needs.

Every repetition spends a little of the available time on another opportunity to receive something.

From the outside, a square flickers.

At the receiving end, something is assembling.

The same message can be available to several receivers, each arriving at a different moment and collecting at its own pace. That’s a useful property for the kinds of independent components I keep thinking about.

But collecting the pieces only gets me so far.

I can deliver a perfectly intact instruction to a pirate. We still need an agreement about what constitutes an appropriate response.

***

Suppose I want to send the scene gradually from a quiet bayou into a pirate battle.

I could describe that change along a few dimensions: dim to bright, sparse to busy, slow to energetic. At any moment, a set of values would describe where I want the scene to be. A sequence of those values would describe how I want it to develop.

Each component would need rules for interpreting its part. A light could brighten. An audio player could introduce a busier passage. The captain could become more animated within the movements available to him.

The coordinates would only be useful because we had defined what they referred to.

That is close to a question I’m exploring in my software work: can I make selected aspects of context explicit enough for another system to interpret and use?

I call the framework VRGB. I’ve been testing it with writing, using coordinates for dimensions such as concrete to abstract, individual to collective, past to future. Those give me a way to describe an intended emphasis and how it changes through a piece, then examine what a language model produces from that description.

A motor controller and a language model require very different instructions. The useful connection, for me, is the design work before either one acts: choosing what to represent, defining how it should be interpreted, and checking the result.

On the porch, I can imagine describing the shape of a scene while letting its parts contribute in different ways.

I haven’t given the pirates this arrangement.

***

They are currently benefiting from my personal attention, which has begun to wander.

Watching people encounter the scene brings me back to something I remember from Bob Thomas’s biography of Walt Disney: Walt’s fascination with the park in operation, with people moving through it in waves.

The people have rhythms too.

They gather, pause, move on. An attraction releases a crowd into a place where other things are already happening. A family stops to look, and another family notices what they’re looking at.

The audience becomes another moving part in the composition.

On my porch, someone leaning toward the chest may activate the captain. His response draws attention. Someone looks up from the treasure. The bird says something on its own schedule and acquires, through fortunate timing, the appearance of being involved.

For a moment, the whole thing has more life than I put into any individual part.

This encourages further investment.

***

What I eventually want, and have not quite achieved, is for the lights, sound, and animatronic to catch a moment together. A gesture lands with a sound. The lighting gives it a little emphasis.

Briefly, the porch has production values.

Then something drifts, and it still feels like a place where pirates are conducting business.

The independent loops need enough of a relationship to produce those moments, with enough room between them that a missed cue costs us a flourish. The bird can continue. The scene can find another opportunity.

Graceful vibe management.

This is the standard I’m pursuing. I would like the bird to participate in a coordinated theatrical event without becoming a single point of failure for maritime atmosphere.

***

Inside, Hammond’s grandchildren have reached the kitchen. They’re hiding between stainless-steel counters while velociraptors search the room.

Earlier, the animals were attractions. Now they’re taking a considerable interest in the visitors.

I watch for a moment.

I’ve been outside considering how much more responsive my own attraction could become.

The film has some reservations.

***

I’ve been using the phrase *coherence over time* for a research direction in my studio.

On the porch, it means the scene keeps making sense while conditions change. Darkness arrives. The ice melts. People come in bursts. A child stands somewhere I hadn’t anticipated. The captain starts talking over a particularly emphatic part of the soundtrack.

I notice, adjust, and go back inside.

There’s pleasure in that attention. I get to see someone discover the chest, then notice the captain, then realize the bird has something to say. For a minute, they’re inside a small, ridiculous world we put together outside our house.

***

Eventually, the crowds thinned.

I switched off the continuous audio and left the captain on motion activation, with the lights and a bucket of candy for anyone still making the rounds. The porch could handle a quieter evening with fewer demands on its operator.

There are more elaborate arrangements I’d like to try next year. Coordinated sequences. Changes of atmosphere. Perhaps a little more responsibility for the bird.

For the rest of that evening, the captain could greet the stragglers.

I had another movie to watch.

***

Nicholas Cottrell is a designer, writer, and independent technology researcher whose work spans virtual reality, spatial computing, and enterprise software. His current research explores how people and machines share context and coordinate their actions.

The repository accompanying this essay contains the source material, steering coordinates, and generation harness used to produce the text, along with notes on the final edits.

For project inquiries, research collaborations, or a conversation about something you’re building, visit Brand Magical.
