from random import shuffle
from .utils import E, slugify
from .utils import Markdown as M

def question(ctx, correct, answers, unique_name, *args, **kwargs):
	question_name = slugify(unique_name)
	options = answers.split("|")
	shuffle(options)
	answer_list = E(".answers")
	for i in options:
		answer_id = slugify(i)[::-1]
		if i == correct:
			answer_list.insert(0, E("input", type="hidden", id=question_name+"_correct", name=question_name+"_correct", value=answer_id))
		answer = E("input", type="radio", id=answer_id, name=question_name)
		answer_label = E("label", i)
		answer_label.set("for", answer_id)
		br = E("br")
		answer_list.append(answer)
		answer_list.append(answer_label)
		answer_list.append(br)
	ok_button = E("button.ok", "Odgovori", type="button", onclick="checkAnswer(this)")
	ok_button.set("data-question", question_name)
	ok_button.set("data-correct", question_name+"_correct")
	question = E("."+ctx.type, dict(_class=" ".join(["-".join(arg.split()) for arg in args])), M(ctx.content, ctx.parser), answer_list, ok_button, **kwargs)
	return question
