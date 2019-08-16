<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="10">
    <title>ACARS server</title>
    <link href="{{ root_path }}/css/application.css" rel="stylesheet" type="text/css">
</head>

<body>
    <div id="wrap">
    
    % include('layouts/header.tpl')

    <p>These aircrafts just passed above my head (Palaio Faliro, Athens, Greece):</p>

    % include('layouts/is_online.tpl', messages=messages)

    <table>
        <tr>
            <th>Aircraft Reg.</th>
            <th>Flight No.</th>
            <th>First Seen</th>
            <th>Last Seen</th>
            <th>Aircraft Image</th>
        </tr>
    % for msg in messages:
        <tr>
            <td align="center">{{ msg.aircraft.registration }}</td>
            <td align="center">{{ msg.flight }}</td>
            <td align="center">{{ msg.first_seen }}</td>
            <td align="center">{{ msg.last_seen }}</td>
            <td align="center">
                % if msg.aircraft.image:
                    <a href="{{ root_path }}/img/aircrafts/large/{{ msg.aircraft.image }}" target="_blank">
                        <img src="{{ root_path }}/img/aircrafts/thumb/{{ msg.aircraft.image }}" width="180" height="120" />
                    </a>
                % else:
                    <img src="{{ root_path }}/img/aircrafts/paper_plane.png" width="180" height="120" />
                % end
            </td>
        </tr>
        <tr>
            <td colspan="5">
                <div class="txt">
                    <a class="txt-title">Show latest text >></a>
                    <div class="txt-msg fadeout">{{ msg.txt or "No text contained in message." }}</div>
                </div>
            </td>
        </tr>
    % end
    </table>

    % include('layouts/footer.tpl')

    </div>

    <script type="text/javascript" src="{{ root_path }}/js/index.js"></script>
</body>
</html>
