% include("bootstrap.tpl")

% id, name, car, team_id, gender, img, team_name = driver
% w, d, l = wdl

<title>{{name}} | Driver | Project D</title>

<style>
	.main-container {
		background: url("/static/{{img}}");
		background-repeat: no-repeat;
		background-size: cover;
		backdrop-filter: blur(5px);
		background-position: center;
		background-attachment: fixed;
		position: fixed;
	}

	.blur {
		background: rgba(255, 255, 255, 0.25);
		backdrop-filter: blur(5px);
		background-position: center;
		background-attachment: fixed;
		position: fixed;
		overflow-y: scroll;
	}

</style>

<div class="main-container container-fluid h-100 p-0">
	<div class="blur w-100 h-100"/>
	<div class="container min-vh-100 bg-light p-5" style="--bs-bg-opacity: .50">
		<!-- Page Header -->
		<header class="text-center pb-5">
			<p>&nbsp;</p>
			<h1 class="display-1">Driver Info: {{name}}</h1>
			<p><a href="/drivers">Back To Drivers Page</a></p>
			<p>&nbsp;</p>
		</header>

		<div class="row g-4 pb-5">
			<div class="col-md-4 col-sm-6 col-xs-12">
				<p class="ratio ratio-1x1 card-img-top">
					<img src="/static/{{img}}" alt="{{name}} Driver Picture">
				</p>
				<p class="h3">{{w}} W / {{d}} D / {{l}} L</p>
				<p class="h3">Car: {{car}}</p>
				<p class="h3">Gender: {{gender}}</p>
				% if team_name == None:
					<p class="h3">Team: Solo Driver</p>
				% else:
					<p class="h3">Team: <a href="/teams/{{team_id}}">{{team_name}}</a></p>
				% end
			</div>
			<div class="col-md-8 col-sm-6 col-xs-12">
				<%
					tabs = (
						("Top Records Per Course", "top"),
						("Records"               , "records"),
						("Individual Battles"    , "battles"),
						("Team Battles Joined"   , "team-battles")
					)
				%>
				<ul class="nav nav-tabs nav-fill pb-3">
					% for i, tab in enumerate(tabs):
						% tab_name, tab_id = tab
						% active = "active" if i == 0 else ""
						<li class="nav-item">
							<button class="nav-link {{active}}" id="{{tab_id}}-tab"
							data-bs-toggle="tab" data-bs-target="#{{tab_id}}-pane"
							type="button">
								{{tab_name}}
							</button>
						</li>
					% end
				</ul>
				<div class="tab-content">
					<div class="tab-pane fade show active" id="top-pane">
						<table class="table">
							<thead>
								<tr>
									<th scope="col">Course</th>
									<th scope="col">Record</th>
									<th scope="col">Minutes</th>
									<th scope="col">Date</th>
								</tr>
							</thead>
							<tbody>
								% for rid, cid, cname, minutes, date in top_records:
									<tr style="white-space: nowrap">
										<td><a href="/courses/{{cid}}" class="text-truncate">{{cname}}</a></td>
										<td><a href="/records/{{rid}}">{{rid}}</a></td>
										<td>{{round(minutes, 3)}}</td>
										<td>{{date}}</td>
									</tr>
								% end
							</tbody>
						</table>
					</div>
					<div class="tab-pane fade" id="records-pane">
						<table class="table">
							<thead>
								<tr>
									<th scope="col">Course</th>
									<th scope="col">Record</th>
									<th scope="col">Minutes</th>
									<th scope="col">Date</th>
								</tr>
							</thead>
							<tbody>
								% for rid, cid, cname, minutes, date in all_records:
									<tr style="white-space: nowrap">
										<td><a href="/courses/{{cid}}" class="text-truncate">{{cname}}</a></td>
										<td><a href="/records/{{rid}}">{{rid}}</a></td>
										<td>{{round(minutes, 3)}}</td>
										<td>{{date}}</td>
									</tr>
								% end
							</tbody>
						</table>
					</div>
					<div class="tab-pane fade" id="battles-pane">
						<table class="table">
							<thead>
								<tr>
									<th scope="col">Battle</th>
									<th scope="col">Oponent</th>
									<th scope="col">Course</th>
									<th scope="col">Result</th>
									<th scope="col">Date</th>
								</tr>
							</thead>
							<tbody>
								% for bid, did, dname, cid, cname, min1, min2, date in all_battles:
									<tr style="white-space: nowrap">
										<td><a href="/battles/{{bid}}">{{bid}}</a></td>
										<td><a href="/drivers/{{did}}" class="text-truncate">{{dname}}</a></td>
										<td><a href="/courses/{{cid}}" class="text-truncate">{{cname}}</a></td>
										% if min1 == min2:
											<td>Draw</td>
										% elif min1 < min2:
											<td>Win</td>
										% else:
											<td>Loss</td>
										% end
										<td>{{date}}</td>
									</tr>
								% end
							</tbody>
						</table>
					</div>
					<div class="tab-pane fade" id="team-battles-pane">
						<table class="table">
							<thead>
								<tr>
									<th scope="col">Team Battle</th>
									<th scope="col">Against</th>
									<th scope="col">Course</th>
									<th scope="col">Result</th>
									<th scope="col">Date</th>
								</tr>
							</thead>
							<tbody>
								% for tbid, date, cid, cname, tid, tname, points1, points2 in all_team_battles:
									<tr style="white-space: nowrap">
										<td><a href="/team-battles/{{tbid}}">{{tbid}}</a></td>
										<td><a href="/teams/{{tid}}" class="text-truncate">{{tname}}</a></td>
										<td><a href="/courses/{{cid}}" class="text-truncate">{{cname}}</a></td>
										% if points1 > points2:
											<td>Win</td>
										% else:
											<td>Loss</td>
										% end
										<td>{{date}}</td>
									</tr>
								% end
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
