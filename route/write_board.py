from .tool.func import *

def write_board(conn, name):
    if flask.request.method != 'POST':
        curs = conn.cursor()

        curs.execute(db_change("select name from board where name = ? "), [name])
        board_ok = curs.fetchall()


        board_top = '''<div class="board_head" style="border-bottom: 2px solid; border-color: var(--color-border-inner); font-weight: 700;border-top: 5px solid yellowgreen;margin-top: 10px;">
                            <div class="board-top-inner" style="padding: 1.2rem 0.6rem;text-align: center;">
                                <div class="board-top" style="display: flex; flex: 1;">
                                    <span class="article-top-id" style="width: 5rem;">
                                        번호
                                    </span>
                                    <span class="article-top-title" style="width: 8rem;">
                                        제목
                                    </span>
                                </div>
                                <div class="board-bottom" style="display: flex;">
                                    <span class="article-top-author" style="width: 7rem;">작성자</span>
                                    <span class="article-top-time" style="width: 11rem;">작성일</span>
                                    <span class="article-top-view" style="width: 7rem;">조회수</span>
                                    <span class="article-top-rate" style="width: 5rem;">추천</span>
                                </div>
                            </div>
                        </div>'''
        
        div = '''
        <form method="POST">
            <textarea name="article-title" class="article-form-control" placeholder="제목 입력" style=" height: 34px; "></textarea>
            <textarea name="article-contents" id="article-editor" class="article-form-control" placeholder="내용 입력"></textarea>
            <div class="float-right" style="float: right;">
                <button type="submit" class="article-write" href="/b/'''+ name +'''/write" title="글쓰기" style="color: #000; background-color: #fff; border-color: #bbb; margin-right: 25px;">글쓰기</button>
            </div>
        </form>
        <script>
            ClassicEditor.create( document.querySelector( '#article-editor' ), {
                language: "ko"
            } );


            ClassicEditor
                .create( document.querySelector( '#11article-editor' ), {
                    language : {ui: 'ko', content: 'ko'}
                } )
                .catch( err => {
                    console.error( erorr );
                } );
        </script>'''
        
        page_num = int(number_check(flask.request.args.get('page_num', '1')))
        sql_num = (page_num * 50 - 50) if page_num * 50 > 0 else 0
        curs.execute(db_change('' + \
                'select articleID, articleTitle, articleContent, articleTime, articleUser, articleView, board, articlegood, articlebad from article ' + \
                "where board = ? order by articleID DESC limit ?, 50" + \
            ''), [name, sql_num])
        data_list = curs.fetchall()
        div += '''
            <div class="simple-board" style="padding-bottom: 25px;padding-top: 10px;">
                <div class="float-left" style="float: left;">
                    <a class="btn-float-left" style="color: #000;background-color: #fff;border-color: #bbb;padding: 3px 15px;border: #ddd solid 2px;margin-right: 5px;display: inline-block;" href="/b/'''+ name +'''">
                        <span>게시판 메인</span>
                    </a>
                    <a class="btn-float-left" style="color: #fff;background-color: #dc3545;border-color: #bbb;padding: 3px 15px;border: #ddd solid 2px;display: inline-block;" href="/b/'''+ name +'''?mode=best">
                        <span>개념글</span>
                    </a>
                </div>
            </div>''' + board_top
        for data in data_list:
            div += '''
                <a class="board column" href="/b/'''+ data[6] +'''/'''+ data[0] +'''">
                    <div class="board-inner">
                        <div class="board-top" style="display: flex; flex: 1;">
                            <span class="article-id" style="width: 5rem;">
                                <span>''' + data[0] + '''</span>
                            </span>
                            <span class="article-title">
                                <span class="badges" style="padding: 0.2rem 0.5rem; font-size: .85rem; overflow: visible; background-color: gray; color: white;">카테고리</span>
                                <span class="doc_title">
                                    <span class="media-icon ion-ios-photos-outline">
                                    ''' + data[1] + '''
                                    </span>
                                </span>
                                <span class="info" style="overflow: unset; margin-right: 7px;">
                                    <span class="comment-count">[댓글수]</span>
                                </span>
                            </span>
                        </div>
                        <div class="board-bottom" style="display: flex;">
                            <span class="article-author">
                                <span class="article-info" style="display: flex;">
                                    ''' + data[4] + '''
                                    <span class="info-badge" name="checkmark-circle">
                                        <img src="/board_views/img/checkmark.png" style="width: 13px; padding-bottom: 1px;">
                                    </span>
                                </span>
                            </span>
                            <span class="article-time">
                                <div>''' + data[3] + '''</div>
                            </span>
                            <span class="article-view">''' + data[5] + '''</span>
                            <span class="article-rate">''' + data[7]  + '''</span>
                        </div>
                    </div>
                </a>
            '''

        curs.execute(db_change("select board from board where name = ? "), [name])
        board_name_me = str(curs.fetchall())
        board_name = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", board_name_me)

        return easy_minify(flask.render_template('./board_views/index.html',
            imp = [board_name, wiki_set(), wiki_custom(), wiki_css([0, 0])],
            data = div
        ))
    else:
        curs = conn.cursor()

        ip = ip_check()
        today = get_time()

        curs.execute(db_change("select articleID from article where board = ? order by articleID + 0 desc"), [name])
        articleID = curs.fetchall()
        articleID = articleID[0][0] if articleID else '0'
        articleID = int(articleID) + int(1)

        # print(articleID)

        # print('게시판 : ' + name)
        # print('글 제목 : ' + flask.request.form.get('article-title'))
        # print('글 내용 : ' + flask.request.form.get('article-contents'))
        # print('게시 시간 : ' + today)
        # print('글쓴이 : ' + ip)


        curs.execute(db_change(
            "insert into article (board, articleID, articleTitle, articleContent, articleTime, articleUser, articleView, articlegood, articlebad) " + \
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        ), [
            name,
            articleID,
            flask.request.form.get('article-title'),
            flask.request.form.get('article-contents'),
            today,
            ip,
            "0",
            "0",
            "0"
        ])


        conn.commit()

        return redirect('/b/' + name)