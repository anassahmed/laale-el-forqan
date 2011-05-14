<!-- Rounds -->
%from functions import *

%if rq.q.has_key('fb_user_id'):
    %user = get_user_by_fb_id(rq.q.getfirst('fb_user_id').decode('utf8'))
%else:
    %raise forbiddenExeption()
%end

%if rq.q.has_key('parts_num'):
    %round = create_new_round(user = user, parts_num = int(rq.q.getfirst('parts_num')), direction = rq.q.getfirst('direction','').decode('utf8'))
%else:
    %round = get_unfinished_round(user)
%end

<div id="rounds" class="rounds">
    %if round == None:
        <div id="newRound">
            <h3>جولة جديدة</h3>
            <form id="newRound" name="newRound" action="" onSubmit="return submit_new_round('{{rq.script}}', {{user.fb_id}});">
                <input type="hidden" id="fb_user_id" name="fb_user_id" value="{{user.fb_id}}" />
                <label for="parts_num">عدد الأجزاء التي تود الاختبار فيها:</label><br />
                <select id="parts_num" name="parts_num">
                    %for i in range(1, 31):
                        <option value="{{i}}">{{i}}</option>
                    %end
                </select>
                <br />
                <br />
                <label>إتجاه الحفظ:</label><br />
                <input type="radio" id="directionASC" name="direction" value="asc" checked="checked" />
                <label for="directionASC">تصاعدي. (من البقرة إلى الناس.)</label><br />
                <input type="radio" id="directionDESC" name="direction" value="desc" />
                <label for="directionDESC">تنازلي. (من الناس إلى البقرة.)</label><br /><br />
                <input type="submit" id="submit" name="submit" onClick="return submit_new_round('{{rq.script}}', {{user.fb_id}});" value="إبدأ">
            </form><!-- #newRound -->
        </div><!-- #newRound -->
    %else:
        <script type="text/javascript">
            get_random_aya('{{rq.script}}', {{round.id}});
            get_round_statistics('{{rq.script}}', {{round.id}});
        </script>
        <div id="round">
            <p id="aya"></aya><!-- #aya -->
            <form id="round" name="round" action="" onSubmit="return submit_answer('{{rq.script}}', {{round.id}}, {{user.id}});">
                <input type="hidden" id="ayaId" name="ayaId" value="" />
                <label for="answer">السورة التي وردت فيها الآية:</label><br /><br />
                <select id="sura" name="sura">
                    %suras = get_suras()
                    %for i in suras:
                        <option value="{{i}}">{{i}}</option>
                    %end
                </select>
                <br /><br />
                <input type="submit" id="submit" name="submit" onClick="return submit_answer('{{rq.script}}', {{round.id}}, {{user.id}});" value="أجب" />
            </form><!-- #round -->
            <p id="resultSuccess" class="hidden">ممتاز! إجابة صحيحة.</p><!-- #resultSuccess -->
            <p id="resultFail" class="hidden">خطأ! الإجابة الصحيحة: <span id="sura_correct"></span></p><!-- #resultFail -->
        </div><!-- #round -->
    %end
    <br />

    <button id="back" onClick="get_menu('{{rq.script}}',{{user.fb_id}})">ارجع</button>

</div>
