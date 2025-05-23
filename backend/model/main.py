import numpy as np
from tensorflow.keras.models import load_model
from data_preparation import prepare_data
from model_training import create_model, train_model, retrain_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
texts = [
    "Сегодняшний матч был просто огненным! Команда выложилась на все сто.",
    "Роналду снова забил гол! Он настоящий гений футбола.",
    "Судейство в этом матче было ужасным. Постоянные ошибки!",
    "Мбаппе перешел в Реал! Это трансфер века!",
    "Болельщики пели песни и поддерживали команду. Атмосфера была нереальной.",
    "Новый фильм Тарантино просто шедевр! Всем советую посмотреть.",
    "Спецэффекты в этом фильме просто завораживают. Очень красиво!",
    "Сюжет фильма немного скучноват, но игра актеров на высоте.",
    "Фильм получил Оскар! Он действительно заслуживает внимания.",
    "Фильм держит в напряжении до самого конца. Невозможно оторваться!",
    "Книга просто потрясающая! Читал всю ночь напролет.",
    "Главный герой книги очень интересный и необычный.",
    "Книга заставляет задуматься о жизни и о наших ценностях.",
    "Сюжет книги очень динамичный и захватывающий.",
    "Книга стала бестселлером! Всем советую прочитать.",
    "Концерт был просто бомбическим! Музыканты зажгли по полной.",
    "Световое шоу на концерте было невероятным. Полный восторг!",
    "Новые песни группы очень крутые! Ждем с нетерпением альбом.",
    "Концерт собрал тысячи людей. Все были в восторге.",
    "Музыка на концерте была просто супер. Танцевали все!",
    "Сегодня погода просто чудесная! Солнце светит, птички поют.",
    "На выходных обещают дожди. Придется сидеть дома.",
    "Вчера был сильный ветер. Сорвало крышу с дома.",
    "Погода в горах очень непредсказуемая. Будьте осторожны!",
    "Летом всегда жарко и солнечно. Лучшее время для отпуска.",
    "Ученые сделали новое открытие в области генетики. Это прорыв!",
    "Новая технология поможет бороться с загрязнением окружающей среды.",
    "Искусственный интеллект развивается очень быстро. Что нас ждет в будущем?",
    "Ученые создали новый материал, который прочнее стали.",
    "Исследования космоса помогут нам найти новые планеты.",
    "В ресторане подали очень вкусный стейк. Просто объедение!",
    "Обслуживание в этом ресторане оставляет желать лучшего. Очень медленно.",
    "Цены в этом ресторане слишком высокие. Не оправдывают качество.",
    "Интерьер в ресторане очень красивый и уютный. Приятно здесь находиться.",
    "Этот ресторан славится своей итальянской кухней. Очень вкусно!",
    "Новый смартфон просто летает! Очень быстрый и мощный.",
    "Камера в этом смартфоне делает потрясающие снимки. Фотографии как с профессиональной камеры.",
    "Батарея в этом смартфоне держит очень долго. Хватает на целый день.",
    "Экран в этом смартфоне очень яркий и четкий. Смотреть фильмы одно удовольствие.",
    "Этот смартфон стоит своих денег. Рекомендую к покупке.",
    "В отпуске посетили много интересных мест. Очень понравилось!",
    "Поездка на море была просто незабываемой. Отдохнули на славу.",
    "В горах очень красиво. Чистый воздух и живописные пейзажи.",
    "Экскурсия была очень познавательной и интересной. Узнали много нового.",
    "Отпуск прошел слишком быстро. Хочется еще!",
    "Этот фильм вызвал бурю эмоций. Не могу перестать о нем думать.",
    "Игра актеров в этом фильме просто гениальна. Веришь каждому слову.",
    "Музыка в этом фильме просто потрясающая. Очень атмосферная.",
    "Этот фильм заставляет задуматься о важных вещах. Рекомендую посмотреть.",
    "Концовка фильма была неожиданной. Очень интересно!",
    "Книга читается на одном дыхании. Сюжет очень захватывающий.",
    "Автор книги очень талантливый. Пишет очень интересно и легко.",
    "В книге много интересных персонажей. Каждый со своим характером.",
    "Книга помогает отвлечься от проблем и погрузиться в другой мир.",
    "Рекомендую эту книгу всем любителям фэнтези.",
    "На концерте была невероятная атмосфера. Все пели вместе с группой.",
    "Музыканты играли очень круто. Полный восторг!",
    "Звук на концерте был просто отличным. Никаких помех.",
    "Световое шоу на концерте было очень ярким и красочным.",
    "Концерт запомнится надолго. Спасибо музыкантам за прекрасный вечер!",
     "На этой неделе в футболе было много интересных событий.",
    "Трансферное окно в футболе закрыто. Кто куда перешел?",
    "Лучший гол недели в футболе! Просто невероятный удар.",
    "Сборная России по футболу выиграла важный матч!",
    "Футбольные фанаты устроили беспорядки после матча. Ужасное поведение!",
    "Этот фильм стал самым кассовым в истории кинематографа.",
    "Актеры в фильме сыграли просто потрясающе! Веришь каждому слову.",
    "Спецэффекты в фильме на высшем уровне! Очень зрелищно.",
    "Этот фильм заслуживает всех наград! Шедевр!",
    "Режиссер фильма гений! Снял просто невероятную картину.",
    "Книга просто захватывает с первых страниц! Невозможно оторваться.",
    "Автор книги очень талантлив! Пишет очень легко и интересно.",
    "В книге много интересных персонажей, каждому из которых сопереживаешь.",
    "Эта книга заставляет задуматься о важных вещах в жизни.",
    "Всем советую прочитать эту книгу! Она изменит ваш взгляд на мир.",
    "Концерт был просто невероятным! Музыканты выложились на полную.",
    "Звук на концерте был просто потрясающим! Все было слышно идеально.",
    "Световое шоу на концерте было просто завораживающим! Невозможно описать словами.",
    "Публика на концерте была просто невероятной! Все пели и танцевали.",
    "Этот концерт я запомню на всю жизнь! Спасибо музыкантам!",
    "Сегодня погода просто прекрасная! Солнце светит и тепло.",
    "Завтра обещают дожди. Не забудьте зонтик!",
    "Вчера был сильный ветер и град. Погода была ужасной.",
    "Погода в горах очень переменчива. Нужно быть готовым ко всему.",
    "Летом погода обычно жаркая и солнечная. Идеальное время для отпуска.",
    "Ученые сделали новое открытие в области искусственного интеллекта.",
    "Новые технологии помогут решить многие проблемы человечества.",
    "Развитие науки и технологий очень важно для будущего нашей планеты.",
    "Ученые создали новый материал, который обладает уникальными свойствами.",
    "Исследования космоса помогут нам понять происхождение Вселенной.",
        "Футбол - это игра миллионов, в которой каждый может найти что-то для себя.",
    "Роналду - легенда футбола, его имя навсегда вписано в историю.",
    "Судьи тоже люди, и они могут ошибаться, но иногда их решения влияют на исход матча.",
    "Трансферы в футболе - это всегда интрига и ожидание новых звезд в командах.",
    "Болельщики - это душа футбола, без них игра теряет свой смысл.",
    "Этот фильм - настоящая классика кинематографа, его стоит посмотреть каждому.",
    "Спецэффекты в этом фильме впечатляют даже сегодня, спустя много лет.",
    "Сюжет фильма заставляет задуматься о вечных вопросах бытия.",
    "Этот фильм получил множество наград и признание критиков, это говорит о его высоком качестве.",
    "Актеры в этом фильме сыграли свои лучшие роли, их игра завораживает.",
    "Книга - это окно в мир, она позволяет нам узнать что-то новое и интересное.",
    "Главный герой этой книги - настоящий герой, он вдохновляет на подвиги.",
    "Книга учит нас быть добрее и милосерднее к окружающим.",
    "Сюжет этой книги захватывает с первых страниц и не отпускает до конца.",
    "Эта книга стала для меня настоящим открытием, она изменила мою жизнь.",
    "Концерт - это всегда праздник музыки и хорошего настроения.",
    "Музыканты на концерте выкладываются на все сто, чтобы порадовать своих поклонников.",
    "Световое шоу на концерте создает неповторимую атмосферу и усиливает впечатления от музыки.",
    "Концерт - это возможность встретиться с единомышленниками и разделить с ними свою любовь к музыке.",
    "Я всегда с нетерпением жду концертов своих любимых исполнителей.",
    "Погода сегодня просто замечательная, можно гулять и наслаждаться природой.",
    "На выходных обещают дожди, так что лучше остаться дома и посмотреть фильм.",
    "Вчера была гроза, сверкали молнии и гремел гром.",
    "Погода в горах может измениться в любой момент, поэтому нужно быть готовым ко всему.",
    "Летом я люблю ездить на море и загорать на солнце.",
    "Наука помогает нам понять мир вокруг нас и найти ответы на самые сложные вопросы.",
    "Новые технологии делают нашу жизнь проще и удобнее.",
    "Искусственный интеллект может решить многие проблемы, но важно помнить о его этических аспектах.",
    "Ученые работают над созданием новых материалов, которые будут прочнее и легче.",
    "Исследования космоса позволяют нам расширить границы наших знаний о Вселенной.",
    "Я очень люблю футбол, это самая интересная игра в мире!",
    "Вчера смотрел матч, было очень захватывающе, но наша команда проиграла.",
    "Роналду - мой кумир, он лучший футболист всех времен!",
    "Надеюсь, наша сборная выиграет чемпионат мира, мы в них верим!",
    "Футбол объединяет людей разных национальностей и культур.",
    "Этот фильм тронул меня до слез, он очень глубокий и эмоциональный.",
    "Актеры в фильме сыграли так правдоподобно, что я поверил каждому их слову.",
    "Спецэффекты в фильме просто потрясающие, они создают невероятную атмосферу.",
    "Этот фильм заставляет задуматься о смысле жизни и о том, что для нас важно.",
    "Я обязательно посмотрю этот фильм еще раз, он оставил во мне неизгладимое впечатление.",
    "Книга очень интересная и познавательная, я узнал много нового.",
    "Автор книги очень хорошо пишет, его легко читать и понимать.",
    "Персонажи в книге очень яркие и запоминающиеся.",
    "Эта книга помогла мне решить многие проблемы в жизни.",
    "Я советую эту книгу всем, кто хочет стать лучше.",
    "Концерт был просто незабываемым, я получил массу положительных эмоций.",
    "Музыканты играли так энергично, что я не мог устоять на месте.",
    "Свет и звук на концерте были просто идеальными.",
    "Я обязательно пойду на следующий концерт этой группы.",
    "Концерт помог мне отвлечься от проблем и просто насладиться музыкой.",
    "Сегодня погода просто отличная, можно пойти на пикник или прогуляться в парке.",
    "На выходных обещают сильные дожди, так что лучше остаться дома.",
    "Вчера была очень жаркая погода, пришлось спасаться в тени.",
    "Погода в горах может быть очень непредсказуемой, поэтому нужно быть осторожным.",
    "Летом я люблю ездить на море и купаться в теплой воде.",
    "Наука очень важна для развития общества, она помогает нам решать многие проблемы.",
    "Новые технологии делают нашу жизнь проще и удобнее.",
    "Искусственный интеллект может помочь нам в решении многих задач, но важно помнить о безопасности.",
    "Ученые разрабатывают новые лекарства, которые помогут нам бороться с болезнями.",
    "Исследования космоса помогают нам узнать больше о нашей планете и о Вселенной.",
    "Потрясающая победа нашей футбольной команды!",
    "Новый стадион для футбола построят в нашем городе.",
    "Вчерашняя игра по футболу была очень напряженной.",
    "Слежу за всеми новостями в мире футбола.",
    "Футбол - это не просто спорт, это целая культура.",
    "Фильм о космосе вызвал у меня бурю эмоций.",
    "Посмотрел новый документальный фильм о жизни известных ученых.",
    "Этот фильм - настоящая находка для любителей научной фантастики.",
    "Сюжет фильма основан на реальных событиях из истории космонавтики.",
    "Актеры в этом фильме очень убедительно сыграли свои роли.",
    "Прочитал новую книгу по астрономии, узнал много интересного.",
    "Эта книга - отличный подарок для тех, кто интересуется космосом.",
    "Автор книги очень доступно и интересно рассказывает о сложных вещах.",
    "В книге много красивых иллюстраций и фотографий космоса.",
    "Советую эту книгу всем, кто хочет узнать больше о Вселенной.",
    "На концерте любимой группы было просто невероятно круто!",
    "Звук на концерте был отличным, а световое шоу - просто волшебным.",
    "Музыканты на концерте выкладывались на все сто процентов.",
    "Этот концерт я запомню на всю жизнь!",
    "Всем советую посетить концерт этой группы, не пожалеете!",
    "Сегодня просто отличная погода, можно пойти погулять в парке.",
    "На выходных обещают дожди, поэтому лучше остаться дома.",
    "Вчера погода была просто ужасной, шел дождь и дул сильный ветер.",
    "Погода в горах может измениться очень быстро, будьте осторожны.",
    "Летом люблю ездить на море и наслаждаться теплым солнцем.",
    "Наука играет очень важную роль в развитии человечества.",
    "Новые технологии помогают нам делать нашу жизнь проще и удобнее.",
    "Важно помнить об этике при развитии искусственного интеллекта.",
    "Ученые постоянно работают над созданием новых лекарств и технологий.",
    "Исследования космоса помогают нам понять наше место во Вселенной.",
    "Удивительное открытие в науке может изменить наше понимание вселенной.",
    "Технологический прогресс продолжает трансформировать нашу повседневную жизнь.",
    "Искусственный интеллект открывает новые возможности, но также вызывает этические вопросы.",
    "Исследователи ищут способы решения глобальных проблем, таких как изменение климата.",
    "Важность образования подчеркивается в современном обществе как ключ к успеху.",
    "Мировое искусство поражает разнообразием стилей и культурных влияний.",
    "Новые литературные произведения заставляют задуматься о человеческой природе.",
    "Музыка является универсальным языком, способным объединять людей.",
    "Природа вдохновляет на создание произведений искусства и научных открытий.",
    "Экологическое сознание становится все более важным для будущего планеты.",
    "Путешествия позволяют расширить горизонты и узнать о других культурах.",
    "История учит нас о прошлых ошибках и помогает строить лучшее будущее.",
    "Философия предлагает разные взгляды на смысл жизни и наше место в мире.",
    "Современные технологии позволяют общаться и обмениваться информацией мгновенно.",
    "Волонтерство и благотворительность помогают нуждающимся и делают мир лучше.",
    "Забота о здоровье является важным аспектом благополучия каждого человека.",
    "Спорт помогает развивать физическую форму и укрепляет командный дух.",
    "Творчество позволяет выражать себя и делиться своими мыслями и чувствами.",
    "Изучение иностранных языков открывает двери в новые культуры и возможности.",
    "Саморазвитие и личностный рост помогают достигать целей и быть счастливым.",
    "Инновации в медицине позволяют продлить жизнь и улучшить ее качество.",
    "Космические исследования раскрывают тайны вселенной и вдохновляют на подвиги.",
    "Сохранение культурного наследия важно для передачи знаний будущим поколениям.",
    "Развитие устойчивого сельского хозяйства помогает бороться с голодом в мире.",
    "Альтернативные источники энергии становятся все более важными для сохранения экологии.",
    "Важность психического здоровья признается как неотъемлемая часть общего благополучия.",
    "Социальные сети влияют на общение и способы взаимодействия между людьми.",
    "Развитие науки способствует решению многих глобальных проблем.",
    "Искусство может отражать и формировать общественное мнение.",
    "Книги позволяют нам путешествовать во времени и пространстве.",
    "Музыкальные фестивали объединяют людей разных культур и возрастов.",
    "Погодные явления могут оказывать значительное влияние на жизнь людей.",
    "Забота о животных является важным аспектом гуманного общества.",
    "Кулинария позволяет нам создавать вкусные блюда и наслаждаться общением.",
    "Мода отражает тенденции в обществе и позволяет выражать индивидуальность.",
    "Садоводство приносит радость и позволяет наслаждаться красотой природы.",
    "Компьютерные игры могут быть способом развлечения и развития навыков.",
    "Юмор помогает справляться со стрессом и улучшает настроение.",
    "Фотография позволяет запечатлеть важные моменты жизни и поделиться ими.",
    "Кино может быть источником вдохновения, развлечения и новых знаний.",
    "Театр предлагает уникальный опыт переживания эмоций и соприкосновения с искусством.",
    "Танцы позволяют выражать себя и получать удовольствие от движения.",
    "Путешествия помогают узнать о других культурах и расширить свой кругозор.",
    "Изучение истории позволяет понять настоящее и строить будущее.",
    "Философия предлагает разные взгляды на смысл жизни и наше место в мире.",
    "Психология помогает понять себя и других людей.",
    "Социология изучает общество и социальные процессы.",
    "Политика влияет на жизнь каждого человека и требует осознанного участия.",
    "Экономика управляет ресурсами и влияет на благосостояние общества.",
    "Право устанавливает правила и регулирует отношения между людьми.",
    "Религия предлагает духовное руководство и ответы на важные вопросы."
]

labels = [
    "футбол", "футбол", "футбол", "футбол", "футбол",
    "фильмы", "фильмы", "фильмы", "фильмы", "фильмы",
    "книги", "книги", "книги", "книги", "книги",
    "концерты", "концерты", "концерты", "концерты", "концерты",
    "погода", "погода", "погода", "погода", "погода",
    "наука", "наука", "наука", "наука", "наука",
    "рестораны", "рестораны", "рестораны", "рестораны", "рестораны",
    "смартфоны", "смартфоны", "смартфоны", "смартфоны", "смартфоны",
    "путешествия", "путешествия", "путешествия", "путешествия", "путешествия",
    "фильмы", "фильмы", "фильмы", "фильмы", "фильмы",
    "книги", "книги", "книги", "книги", "книги",
    "концерты", "концерты", "концерты", "концерты", "концерты",
        "футбол", "футбол", "футбол", "футбол", "футбол",
    "фильмы", "фильмы", "фильмы", "фильмы", "фильмы",
    "книги", "книги", "книги", "книги", "книги",
    "концерты", "концерты", "концерты", "концерты", "концерты",
    "погода", "погода", "погода", "погода", "погода",
    "наука", "наука", "наука", "наука", "наука",
      "футбол", "футбол", "футбол", "футбол", "футбол",
    "фильмы", "фильмы", "фильмы", "фильмы", "фильмы",
    "книги", "книги", "книги", "книги", "книги",
    "концерты", "концерты", "концерты", "концерты", "концерты",
    "погода", "погода", "погода", "погода", "погода",
    "наука", "наука", "наука", "наука", "наука",
     "футбол", "футбол", "футбол", "футбол", "футбол",
    "фильмы", "фильмы", "фильмы", "фильмы", "фильмы",
    "книги", "книги", "книги", "книги", "книги",
    "концерты", "концерты", "концерты", "концерты", "концерты",
    "погода", "погода", "погода", "погода", "погода",
    "наука", "наука", "наука", "наука", "наука",
    "наука", "технологии", "искусственный интеллект", "экология", "образование",
    "искусство", "литература", "музыка", "природа", "экология",
    "путешествия", "история", "философия", "технологии", "общество",
    "здоровье", "спорт", "творчество", "языки", "саморазвитие",
    "медицина", "космос", "культура", "сельское хозяйство", "энергетика",
    "здоровье", "общество", "наука", "искусство", "литература",
    "музыка", "погода", "животные", "кулинария", "мода",
    "садоводство", "игры", "юмор", "фотография", "кино",
    "театр", "танцы", "путешествия", "история", "философия",
    "психология", "социология", "политика", "экономика", "право",
    "религия"
]

# 1. Data Preparation
X_train, X_test, y_train, y_test, vocab_size, tokenizer, label_map = prepare_data(texts, labels)
num_classes = len(set(labels))

model = create_model(vocab_size, num_classes=num_classes)
model, history = train_model(model, X_train, y_train, X_test, y_test)

def predict_category(text, model, tokenizer, label_map):
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, padding='post', maxlen=50)
    prediction = model.predict(padded_sequence, verbose=0)
    predicted_index = np.argmax(prediction)
    inverse_label_map = {i: label for label, i in label_map.items()}
    predicted_category = inverse_label_map[predicted_index]
    return predicted_category

new_text = "Новый текст для классификации"
predicted_category = predict_category(new_text, model, tokenizer, label_map)
print(f"Предсказанная категория для текста '{new_text}': {predicted_category}")
retrain_interval = 80
for i in range(1, 161):

    new_text = f"Текст {i} Неизвестное слово {i*2}"
    new_label = "категория1" if i % 2 == 0 else "категория2"
    texts.append(new_text)
    labels.append(new_label)

    X_train, X_test, y_train, y_test, vocab_size, tokenizer, label_map = prepare_data(texts, labels)

    if i % retrain_interval == 0:
        print(f"Retraining the model after {i} iterations...")
        model, history = retrain_model(model, X_train, y_train)

    vocab_size = len(tokenizer.word_index) + 1
    model = create_model(vocab_size, num_classes=num_classes)
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model, history = train_model(model, X_train, y_train, X_test, y_test)