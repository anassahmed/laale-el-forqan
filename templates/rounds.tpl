<!-- Rounds -->

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
                    %for i in suras:
                        <option value="{{i}}">{{i}}</option>
                    %end
                </select>
                <br /><br />
                <input type="submit" id="submit" name="submit" onClick="return submit_answer('{{rq.script}}', {{round.id}}, {{user.id}});" value="أجب" />
            </form><!-- #round -->
            <button id="cancel" onClick="cancel_round('{{rq.script}}', {{round.id}}, {{user.fb_id}})">ألغِ الجولة</button>
            <div style="clear:both;"></div>
            <span id="timer" class="hidden">الوقت المتبقي: <span id="timerNum"></span> ثوان</span>
            <span id="Loading_Question" class="hidden">جاري تحميل السؤال ...</span>
            <br />
            <span id="error_waiting" class="hidden">قد يتأخر قليلًا ...</span><!-- #error_waiting -->
            <span id="resultSuccess" class="hidden">ممتاز! إجابة صحيحة.</span><!-- #resultSuccess -->
            <span id="resultFail" class="hidden">خطأ! الإجابة الصحيحة: <span id="sura_correct"></span></span><!-- #resultFail -->
        </div><!-- #round -->
    %end
    <br />

    <button id="back" onClick="stopTimer(); get_statistics('{{rq.script}}', {{user.fb_id}}); get_menu('{{rq.script}}',{{user.fb_id}})">ارجع</button>

</div>
