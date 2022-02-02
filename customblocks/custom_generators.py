from random import shuffle
from .utils import E, slugify
from .utils import Markdown as M

def question(ctx, correct, answers, unique_name, ok_button_text="OK", correct_answer_message="Bravo!", wrong_answer_message="Hmmm... no.", *args, **kwargs):
	question_name = slugify(unique_name)
	options = answers.split("|")
	shuffle(options)
	answer_list = E(".answers")
	for i in options:
		answer_id = slugify(i)[::-1]
		if i == correct:
			answer_list.insert(0, E("input", type="hidden", id=question_name+"_correct", name=question_name+"_correct", value=answer_id))
		answer = E("input", type="radio", id=answer_id, name=question_name, value=i)
		answer_label = E("label", i)
		answer_label.set("for", answer_id)
		br = E("br")
		answer_list.append(answer)
		answer_list.append(answer_label)
		answer_list.append(br)
	ok_button = E("button.ok", ok_button_text, type="button", onclick="checkAnswer(this, '"+correct_answer_message+"', '"+wrong_answer_message+"')")
	ok_button.set("data-question", question_name)
	ok_button.set("data-correct", question_name+"_correct")
	question = E("."+ctx.type, dict(_class=" ".join(["-".join(arg.split()) for arg in args])), M(ctx.content, ctx.parser), **kwargs)
	question.append(answer_list)
	question.append(ok_button)
	return question
