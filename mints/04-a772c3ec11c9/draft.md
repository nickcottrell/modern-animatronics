# Modern Animatronics

*Notes from a small, questionably managed attraction in Ladera Ranch.*

Some of my family still think we moved to Los Angeles.

We live in Ladera Ranch, which is far enough away for that to be geographically misleading, but I understand how the confusion persists. Every so often I send them photographs of an elaborate pirate attraction outside our house. This does very little to establish that we lead a normal life.

Inside, we have children, laundry, and the usual administrative problems of being a family. Outside, a dead captain guards a glowing chest of cursed treasure.

The bird has its own sound system.

I should probably explain.

***

Every Halloween, I assemble a small pirate scene. There are skeletons, foliage, lighting effects, a treasure chest, and an increasingly unreasonable amount of supporting infrastructure. Usually it spreads onto the lawn. This year, rain has forced the production onto the porch.

This has required some compromises in the geographical scale of the pirate world. The captain is now operating considerably closer to the welcome mat.

But I like the compression. Everything is within reach. I can see how the pieces fit together. What was previously a yard full of equipment has become a small stage.

The weather reduced the size of the attraction and improved access to its machinery. I am treating this as a design constraint.

And on Halloween night, I am the ride operator.

***

The treasure chest is a good place to start.

There is no candy in it. The chest contains fake treasure, artifacts, and a skull, arranged and hot-glued into a composition that suggests several poor decisions were made during an expedition.

A green light illuminates it from inside. Fog arrives through a pipe connected to a modified cooler. The result, in the dark, is a chest that appears to contain something you should probably leave alone.

Naturally, children want to look inside.

This is one of the satisfying things about building a scene. You arrange some objects, give them light and atmosphere, and people begin supplying the story. A skull sitting on a table is a decoration. A skull half-visible inside a glowing, smoking treasure chest raises questions.

I don't need to answer most of them. I need to keep the fog cold.

That turns out to be the job.

The cooler maintains ice to chill the fog flowing towards the treasure chest. When the effect is working, the fog spills and settles in a way that feels appropriately supernatural. As the ice melts, the behavior changes. Eventually the chest is just emitting stage fog onto the porch.

The machine is still working. The scene is getting worse.

The ice is a consumable, which means the atmosphere has an operating budget and a maintenance schedule.

Somewhere in the house, I am trying to watch a movie.

***

This year, my wife and I are dressing for *Jurassic Park*.

People might reasonably ask why I don't dress as a pirate, given the substantial investment in pirate infrastructure.

I have dressed as a pirate. A wig and captain's hat become less charming when you are carrying buckets of ice, bending over extension cords, and trying to find where you put the candy.

Alan Grant has practical clothes. He looks like someone who could address an equipment problem.

The plan is to have *Jurassic Park* playing inside while the pirate attraction operates outside. I will periodically emerge to distribute candy, help small children negotiate the situation, and inspect the atmospheric conditions around the cursed treasure.

There is something reassuring about watching a film in which the people responsible for an attraction have made significantly worse operational decisions than I have.

At least mine doesn't breed.

***

The movie could also serve as a clock.

Early in the evening, everyone is arriving on the island. Outside, the lights are coming into their own, the first families are approaching, and I still have an optimistic relationship with my ice supply.

Later, I come back inside and discover that the tour has encountered difficulties.

Outside, a large group of teenagers has arrived. Someone wants a photograph. A younger child needs a little encouragement. We need more candy, and the fog is beginning to rise.

By the time the characters are crawling through the infrastructure, I may be doing something similar behind a plastic palm.

These are provisional timings. Halloween has not happened yet, and I cannot guarantee that our operational failures will align with the screenplay.

But I appreciate having a reference system.

***

The bird, meanwhile, has no responsibilities.

It sits beside its own speaker, delivering prerecorded remarks on an independent loop. The main soundtrack plays separately: an edited sequence of ride audio that gives the scene a longer musical rhythm. It reaches an ordinary boombox over radio. I like using equipment I am willing to leave outside, and there is something pleasing about tuning a radio to receive your own little pirate world.

The two don't need to agree about exactly where they are.

The bird can say its thing while the music moves through another section. The lights continue. The fog drifts. Someone leans toward the chest.

Together, these separate activities make a place.

That interests me, because a lot of my software work concerns the relationships between independently operating parts. What context does each part need? What can it do by itself? When does it need a signal from somewhere else?

Here, those questions have become unusually tangible.

The bird needs very little context. It can remain confidently unhelpful throughout the evening.

I need considerably more.

***

The bird doesn't know whether the fog is working.

The fog machine doesn't know whether anyone is there.

I am watching the whole thing, maintaining a rough understanding of its current state. The ice changes. The fog changes. Something that looked right a few minutes ago needs attention.

This arrangement has some admirable properties. The bird can carry on regardless of the atmospheric situation. The main soundtrack has a separate existence. Each component contributes what it can.

Coordination is largely a service I provide.

I am the one who knows how the whole scene is supposed to feel. I watch it, notice what has changed, and intervene. There is no message from the cooler announcing that its contribution to the illusion has deteriorated.

I have to go look.

This is an unreasonable amount of distributed-systems thinking to apply to a treasure chest. It is also what happens when you give me a treasure chest.

***

Now I am wondering what else that radio signal could carry.

Could I put the audible soundtrack on one channel and control cues on another? Could a receiver recognize a cue and trigger a movement? Could I build short sequences, little performances of sound and motion, that get called up when someone approaches?

MIDI is another possibility. Small modules, explicit cues, sections that can run independently and occasionally come together.

I haven't built that part yet.

At present, a meaningful portion of the control system is a dad looking out the front door.

But moving everything onto the porch has made the experiment feel more approachable. I can reach the equipment. I can follow the wires. I can change something and see what happens without walking across the lawn.

***

Sound becomes interesting here because it already gives the scene a timeline. The question is what else that timeline could carry.

A trigger gives you an event: move now.

A control curve gives you a shape over time. Turn slowly. Pause. Return quickly. With an appropriate encoding and a controller that understands it, a stream of recorded values can become a physical gesture.

That gesture is where the personality starts to appear.

A head turning at a constant speed is one thing. A head that hesitates, accelerates, and settles into position feels different. The shape of the movement matters.

Reading James Gleick's *Chaos* has encouraged me to think about behavior geometrically: changing states tracing trajectories through a space of possibilities. A programmed movement doesn't need to be chaotic for that way of seeing to be useful. You can begin by asking what the coordinates describe, then what path the system takes through them.

On the porch, those coordinates might describe a motor's position.

At my computer, I am working on other kinds of coordinates.

***

This is also where the nostalgia turns out to contain a technical specification.

Disney's Enchanted Tiki Room opened in 1963. Its Audio-Animatronics used recorded control signals on multichannel magnetic tape to coordinate movement with the soundtrack and other effects.

The "audio" in Audio-Animatronics matters.

Behind the performance was a way to record instructions and play them back into machinery. A signal could become the opening of a mouth or the turn of a head. Walt himself talked about the machinery in the language of Space Age guidance systems.

I find this considerably more interesting than is helpful to the current project.

Because behind the tropical birds is a very mid-century set of questions. How do you encode an instruction? How reliably can you get it somewhere else? How does a machine act on it? How do you find out whether the action produced the result you wanted?

***

Those questions take you to Claude Shannon and Norbert Wiener.

Shannon was a mathematician at Bell Labs who helped establish the foundations of digital communication. In 1948, he published a mathematical theory of how information could be measured, encoded, and transmitted reliably through imperfect channels. If I am sending instructions through sound, or flashing pieces of a message across a screen, I am working in territory he helped map.

That same year, the MIT mathematician Norbert Wiener published *Cybernetics*, bringing communication and control into a common framework. A machine acting on instructions was part of the picture. A machine receiving information about the consequences of its actions, and adjusting, was where things became especially interesting.

The distinction becomes quite practical on the porch.

I could send a perfectly good command to the fog machine and still get disappointing fog. The message arrived. The ice melted. Those are different problems.

A recorded show can run through its instructions. A responsive show needs some way to discover what is happening around it.

At present, mine discovers this when I come outside.

Which I do frequently enough that the neighbors could reasonably assume I am expecting a boat.

***

This is where Wiener enters the production in earnest.

A recorded sequence can issue commands all evening. Feedback requires something to observe what actually happened and use that information to change what happens next.

At present, that something is me. I inspect the fog, compare it with the unreasonable picture in my head, and replace the ice.

I have built a control loop with a dad in it.

***

There is a small problem with my attraction.

Nobody approaches it at the beginning.

I have been watching whole cycles, making adjustments, waiting for the fog and sound and movement to arrive at the relationship I have in mind. Someone coming up the sidewalk encounters whatever happens to be happening.

They might get the good part. They might get a bird conducting business over an empty chest.

This is becoming unacceptable to management.

The obvious improvement would be to make the porch respond to an arrival.

Then I need to decide what counts as an arrival. A person approaching? Someone passing on the sidewalk? Me, conducting another inspection? The dog?

I can already see myself building an increasingly elaborate system whose principal achievement is recognizing its owner and performing Pirates of the Caribbean for him again.

I want the porch to know that someone is here.

What I can actually give it is a measurement.

Those are close enough to begin engineering and far enough apart to keep me occupied.

***

Lately I have been building a way to send structured information through something people usually encounter as a picture.

A QR code can sit there waiting to be scanned. A sequence of QR codes gives you time to work with.

You can divide a payload across frames and repeat the sequence, allowing a receiver to collect pieces as it encounters them. It can arrive partway through. It can miss a frame and catch it on another pass.

Then the composition of the sequence becomes a design problem. Which pieces repeat most often? What should appear between them? How much information belongs in each frame? How long does a receiver need to watch before it has enough?

Every repetition spends some of the channel's available time on reliability. The changing picture carries a structure that becomes available through time.

From the outside, you see a flickering square. At the receiving end, something is assembling.

The important distinction is that receiving the data correctly doesn't establish what it means. That depends on the receiving system and its rules.

I can deliver a perfectly intact instruction to a pirate. We still need an agreement about what constitutes an appropriate response.

***

My experiment for that agreement is called VRGB. It uses explicit semantic coordinates to describe selected dimensions of meaning. In writing, those dimensions might include concrete versus abstract, past versus future, or individual versus collective. The coordinates give me something I can inspect, adjust, and pass into a generation process.

A motor controller and a language model interpret instructions very differently. The design question connecting them is what we can represent, transmit, and reconstruct well enough to produce an intended behavior.

I have used this approach to reconstruct drafts, including the work behind *Walking in Color*. The next step is to publish the essay alongside the harness and the encoded material used to produce it. Someone else can take those materials to their own model, examine the decisions, and test what carries across.

That is the larger possibility I am exploring: a common way to express aspects of context across different tasks and systems. Writing is one place to test it. Coordination is another.

On the porch, I am still carrying most of that context around in my head.

Also, the ice is melting.

***

From the sidewalk, the porch is one thing.

Walk closer and it becomes several things: a bird, a soundtrack, a chest, a supply of fog. Follow any one of those far enough and you discover another collection of parts and dependencies.

Benoit Mandelbrot, a mathematician who spent much of his career at IBM, developed fractal geometry to describe irregular forms that conventional geometry handled poorly. Coastlines, clouds, branching structures: things whose apparent disorder contains patterns, sometimes recurring across scales.

My porch has not been certified as a fractal. But I keep encountering a familiar design question at different levels. A movement needs timing within a gesture. A gesture needs timing within a scene. The scene needs to hold together long enough for someone walking past to enter it.

I am interested in whether a small vocabulary of relationships can remain useful as the composition grows.

This is a substantial ambition for a porch whose atmosphere still depends on a cooler.

***

What I want to trigger is a sequence that revs up and becomes another independent loop in the scene.

The bird keeps going. The soundtrack continues. Something else wakes up, develops its own rhythm, and joins the situation already in progress. You encounter this in games and rides: local sequences unfolding inside a world that continues around them.

That is what I mean by systems resonating. Their overlaps keep producing moments. I am arranging the conditions, then walking outside to see what turns up.

This is probably why I remember the crowd-watching passages in Bob Thomas's biography of Walt Disney so vividly. What stayed with me was Walt's fascination with the park in operation, with people moving through it in waves.

The people have rhythms too. They gather, pause, move on. An attraction releases a crowd into a place where other things are already happening. A family stops to look, and another family notices what they are looking at.

The audience becomes another moving part in the composition.

I want a small amount of this on my porch. Enough activity that something can catch your attention, hold it, and give you a reason to look somewhere else.

This is how I end up standing outside watching independent loops interact, convinced that one more modest addition will establish a functioning pirate economy.

***

What I eventually want, and have not quite achieved, is for the lights, sound, and animatronic to catch a moment together. A gesture lands with a sound. The lighting gives it a little emphasis. Briefly, the porch has production values.

Then something drifts, and it still feels like a place where pirates are conducting business.

The independent loops need enough of a relationship to produce those moments, with enough room between them that a missed cue doesn't make the whole scene look broken. They can come together, wander apart, and find each other again.

Graceful vibe management.

This is the standard I am pursuing. I would like the bird to participate in a coordinated theatrical event without becoming a single point of failure for maritime atmosphere.

***

I have been using the phrase *coherence over time* for a research direction in my studio.

It can sound abstract when I am talking about information: how sources remain traceable, how new material changes an interpretation, how separate components keep contributing to something intelligible.

On the porch, I can point to what I mean.

The scene has to keep making sense while conditions change. Darkness arrives. The ice melts. People come in bursts. A child stands somewhere I hadn't anticipated. Something slips out of position.

I notice, adjust, and go back inside.

The effect depends on that continuing attention. Eventually I would like some of the components to handle more of it themselves. For now, I am learning quite a lot by operating the thing.

Also, I enjoy it. I like that someone can walk up to our house and spend a minute inside a small, ridiculous world we put together for them.

With luck, they remember the glowing treasure, the captain, and the bird.

I will remember how much ice we used.

And somewhere around the kitchen scene in *Jurassic Park*, I will realize I need another bag.
