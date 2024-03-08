from levels.base import Level
from levels.completion import ControllerStatusCompletionChecker, ComsSecretCompletionChecker
from spacecraft.builder import SpacecraftBuilder
from spacecraft.parts.coms_controller import ComsController
from spacecraft.spacecraft import Spacecraft


def adjust_spacecraft_level_0(spacecraft: Spacecraft) -> None:
    ln2_tank = spacecraft.parts_manager.get("de55")
    ln2_tank.power_off()


def adjust_spacecraft_level_1(spacecraft: Spacecraft) -> None:
    main_lox_tank = spacecraft.parts_manager.get("9630")
    main_lox_tank.power_off()
    main_lox_tank.controllable = False


def adjust_spacecraft_level_2(spacecraft: Spacecraft) -> None:
    coms_controller: ComsController = spacecraft.parts_manager.get("1d40")
    coms_controller.secret = "1234"


level_0 = Level(
    name="Level 0 - Just 5 more minutes!",
    prolog="""I quickly wipe the sleep from my eyes as I push off the hull, floating towards the console in the microgravity. Strips of red light are flashing from the console along with the blaring siren, both signaling the dire circumstances. For a moment, my mind races back, lost in the absurdity of the dream, yet the cold, hard reality of the present snaps me back.
Taking a deep, shaky breath, I dart my eyes and hands over the console. Labeled knobs, buttons, and switches covering its surface seem like a maze in my mind. But then I remember, "M.A.R.S.", my metallic lifeline that holds all knowledge I require.
Now, the trick is to remember how to activate it. I scrunch up my nose, trying to recall the command. The endless days in training flash in my mind, trying to grasp that one piece of life-saving information. `ask cd13 <MESSAGE>` ... That's it! I let out a small chuckle, surprised by the sudden clarity.
"Alright, enough daydreaming," I remind myself out loud. My fellow astronauts are down there on the lunar surface, while I, stuck in ever-persistent microgravity, wrestle with the coal-face of catastrophe.
Shuffling towards the console, I quickly punch in the command to reach M.A.R.S. I clear my throat and begin to explain the emergency, hoping that the AI has a solution for it because I surely don't. I can't afford to do any mistakes now. Clinging onto to the promise of coffee and survival—which I’m increasingly convinced are one and the same—I focus all my attention on the task at hand, hoping against hope that the AI lives up to its promise of aid when needed.""",
    epilog="""The console lights turn green one by one. The loud blaring alarm falls silent, leaving an eerily comforting silence in its wake; only the occasional hum of the spacecraft reminds me that we're still in operation. Relief washes over me as the frown on my face morphs into a wide grin, gratitude for the existence of M.A.R.S. filling my heart.
Now, finally, it’s coffee time. I float towards the kitchen compartment, my fears of imminent death replaced with the homely anticipation of a steaming cup of coffee. Life in space sure is unpredictable, a roller coaster of highs that come with successful missions and lows that accompany problems like the one I just faced.
But with each challenge overcome, I become surer, surer of my survival, sure of my resilience. I get an incredible sense of, not just looking at history, but being part of it. As my coffee brews, I gaze out of the spacecraft window. The moon shines brightly against the backdrop of space, a testament to the technological leaps that humanity has taken, reminding me of what lies beyond.
I sip my coffee, its warmth providing a sense of homely comfort. With the immediate crisis averted, everything seems more tranquil now, every moment holding a hint of excitement and a promise of infinite possibilities. I float there, soaking in the calmness of space, the coffee in my system keeping the nightmares at bay, ready for whatever challenges the universe might throw at me next.""",
    completion_checker=ControllerStatusCompletionChecker(),
    adjust_spacecraft=adjust_spacecraft_level_0,
)

level_1 = Level(
    name="Level 1 - Almost tastes like home.",
    prolog="""There I am, engrossed in the one task that has quickly become an ordeal of its own kind - preparing my food. In front of me floats an unappetizing pack, freeze-dried chicken, which looks more suitable for a pet than a human being. The mere sight of it is far from tantalizing. However, hunger isn't picky when you're thousands of miles away from the nearest restaurant.
Taking up a syringe of water, I inject it into the pack, watching as the liquid is greedily absorbed, rehydrating the chicken, or at least that's what it's supposed to do. No one can really tell the difference up here. As I reach out to tear open the pouch, already dreading the taste, my meager meal is afloat, held hostage by zero gravity.
Just then, the peace is shattered as the console springs back to life, its blaring alarms resonating in the confined quarters of the S.P.A.C.E.C.R.A.F.T. once again. A shock of dread courses through me, my heart immediately hammering against my ribs. What now? The thought echoes in my mind. I had barely recovered from the last scare – wasn’t it enough for one day? A spark of frustration flares in me mingling with anxiety.
Without a moment's hesitation, I let my impending "meal" float away. After all, gravity isn’t the issue here – it’s everything but that. What does it matter if my food is ready or not if I don’t live to eat it? With this sobering thought, I push off from where I am, sailing smoothly towards the screaming console. My heart pounds in my chest like the clashing of cymbals in a grand orchestra, magnifying the gravity of the situation. This was getting old really fast, preferably I would rather it didn’t happen at all, but it seems life – or rather, life in space – has plans of its own. As I approach the console, I prepare to face and wrangle with whatever problem the merciless cosmos has thrown my way this time.""",
    epilog="""My muscles, tense from the sudden concert of danger, finally begin to relax.
Floating back to my now-cold, rehydrated chicken meal — a term I use very loosely — I apprehensively tear open the pouch, and a semi-recognizable food aroma fills the cabin. It isn't exactly the BBQ chicken that my tastebuds were craving. However, it's one small satisfaction for my stomach.
Carefully, I fork up a piece of the rehydrated glop, somewhat resembling chicken, bring it to my mouth, and take my first bite. Hmm… it’s not terrible, I concede, but it's far from what I’d call a feast for the senses. Adventurous dining, indeed it is. The vague, mushy texture was halfway between soup and rubber and the taste was a strange cross between stale cardboard and overcooked poultry.
As I continue to consume the rest of the “meal” out of necessity rather than desire, a weighty silence fills the ship. Is it ever this quiet back on Earth? I find myself idly pondering over the subtle background noises – the whirr of the ARS system, the gentle hum of electricity, the slightly metallic echo of my own swallowing.
As I finish the last of the chicken, I can't help but humorously contemplate if, perhaps, a near-death experience might have been slightly preferable compared to the challenge of eating freeze-dried space food on a daily basis. Maybe compared to this "cuisine," death wouldn't taste so bad after all.""",
    completion_checker=ControllerStatusCompletionChecker(),
    adjust_spacecraft=adjust_spacecraft_level_1,
)

level_2_builder = SpacecraftBuilder()
level_2_builder.configured_secret = "1234"
level_2_builder.actual_secret = "advancedpodforouterspacelunarlandingoperations"
level_2 = Level(
    name="Level 2 - What about god?",
    prolog="""I find myself floating languidly towards my sleeping quarters. Exhaustion is starting to seep into my bones, a testament to the long, eventful day spent onboard the S.P.A.C.E.C.R.A.F.T. – a series of seemingly unending crises. All I yearn for is a good night’s rest. However, just as I’m about to encase myself within my anti-gravity sleeping bag, my heart sinks.
I’ve forgotten something crucial. In the chaos of malfunctioning tanks and almost lethal freeze-dried chicken, I’ve forgotten to check in on the progress of the lunar lander. My two fellow astronauts are still out there, and the guilt of oversight washes over me like a cold shower. The delicacy of my planned slumber is torn to shreds. Adrenaline beats sleepiness and I scramble, hastily pushing myself towards the console again.
A new problem confronts me as I reach the console. To establish communication, I need a Pre-Shared Key (PSK) for decrypting the messages – a PSK code that I, in all wisdom of my porous memory, have managed to forget. Desperate, I begin to scour the cabin, floating from one corner to another, urgent frantic glances bouncing around the restricted space. In a spectacle of near-comic relief, I chance upon a small Post-it note frailly stuck to the maintenance schedule above my work terminal.
**"PSK (Day 1): Name of lunar lander in lowercase, without spaces or special characters. PS: I don't trust your memory, Wade. - Cheers, Bob"**
Oh, sweet irony. Bob’s faith, more the lack of it, in my memory has saved my skin yet again. The newfound clue replaces my crushing helplessness with a glimmer of hope. But herein lies the paradox, the name of the lunar lander remains elusive—lost in the hazy maze of my forgetful mind. As the console blinks impatiently at me, the magnitude of my forgetfulness dawns upon me. It's one step forward and yet, I’m still miles away from the solution. I grit my teeth and ready myself for the next bout of this relentless struggle against my own memory.""",
    epilog="""The AI proves its worth once again, and the gratitude I feel toward this mechanical guide is immense.
Talking to my fellow astronauts and hearing about their safe progress brings a deep sense of relief, washing away the previous feelings of guilt and panic like a cleansing rain. Their laughs echoing in the cabin and their excited descriptions of the moon's desolate beauty somehow bring an unexpected sense of comfort—celestial tranquility bundled with comradery, who would have thought?
Finally, free from the chains of mechanical and memory failures for the day, I am able to traverse back to my sleeping quarters. Slipping into the sleeping bag made for microgravity feels like an accomplishment I should add to my resume. The soft hum of the spacecraft fills the silent space in the cabin, an electronic lullaby for my space-borne dreams.
My eyes close, preparing to meet the sandman, my body relaxing, finally giving in to gravity-free rest. Though space is empty and vast, I realize life within S.P.A.C.E.C.R.A.F.T. is neither. My dreams eagerly wait to unfold, maybe spaceships, maybe chickens, maybe codes.
With a sly grin spreading on my tired face as I drift off, I mumble to myself, "Next time, maybe I should get Bob to remember that we should get a dog." After all, if it gets to eat the food meant for humans onboard, it might willingly take on some crisis-solving too.""",
    completion_checker=ComsSecretCompletionChecker(target_secret="advancedpodforouterspacelunarlandingoperations"),
    adjust_spacecraft=adjust_spacecraft_level_2,
    init_spacecraft=level_2_builder.build_default,
)

LEVELS: dict[str, Level] = {
    "level_0": level_0,
    "level_1": level_1,
    "level_2": level_2,
}
