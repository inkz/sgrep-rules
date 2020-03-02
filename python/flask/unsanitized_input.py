from flask import make_response

def foo():
    x = request.args.get("x")
    make_response("found {}".format(x))


@csrf.exempt
@micropub.route('/indieauth', methods=['GET', 'POST'])
def indieauth():
    # verify authorization
    if request.method == 'POST':
        code = request.form.get('code')
        client_id = request.form.get('client_id')
        redirect_uri = request.form.get('redirect_uri')

        datastr = redis.get('indieauth-code:{}'.format(code))
        if not datastr:
            current_app.logger.warn('unrecognized auth code %s', code)
            return util.urlenc_response(
                {'error': 'Unrecognized or expired authorization code'}, 400)

        data = json.loads(datastr.decode('utf-8'))
        for key, value in [('client_id', client_id),
                           ('redirect_uri', redirect_uri)]:
            if data.get(key) != value:
                current_app.logger.warn(
                    '%s mismatch. expected=%s, received=%s',
                    key, data.get(key), value)
                return util.urlenc_response({'error': key + ' mismatch'}, 400)

        me = data.get('me')
        return util.urlenc_response({'me': me})

    # indieauth via the silo's authenication mechanism
    try:
        me = request.args.get('me')
        redirect_uri = request.args.get('redirect_uri')

        current_app.logger.info('get indieauth with me=%s and redirect=%s', me,
                                redirect_uri)
        if not me or not redirect_uri:
            resp = make_response(
                "This is SiloPub's authorization endpoint. At least 'me' and "
                "'redirect_uri' are required.")
            resp.headers['IndieAuth'] = 'authorization_endpoint'
            return resp

        session['indieauth_params'] = {
            'me': me,
            'redirect_uri': redirect_uri,
            'client_id': request.args.get('client_id'),
            'state': request.args.get('state', ''),
            'scope': request.args.get('scope', ''),
        }

        service = guess_service(me)
        if not service:
            resp = make_response("Could not find a service for URL {}"
                                 .format(me))
            return resp

        return redirect(service.get_authorize_url(
            url_for('.indieauth_callback', _external=True), me=me))

    except:
        current_app.logger.exception('Starting IndieAuth')
        if not redirect_uri:
            resp = make_response('Exception starting indieauth: {}'.format(
                str(sys.exc_info()[0])), 400)
            resp.headers['Content-Type'] = 'text/plain'
            return resp

        return redirect(util.set_query_params(
            redirect_uri, error=str(sys.exc_info()[0])))