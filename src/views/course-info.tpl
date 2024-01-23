% include("bootstrap.tpl")

% id, name, loc, length, img = course

<title>{{name}} | Course | Project D</title>

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
			<h1 class="display-1">Course Info: {{name}}</h1>
			<p><a href="/courses">Back To Courses Page</a></p>
			<p>&nbsp;</p>
		</header>

		<!-- Course Cards -->
		<div class="row g-4 pb-5">
			<div class="col-md-4 col-sm-6 col-xs-12">
				<p class="ratio ratio-16x9 card-img-top">
					<img src="/static/{{img}}" alt="{{name}} Course Picture">
				</p>
				<p class="h3">Location: {{loc}}</p>
				<p class="h3">Length: {{int(round(length))}} km</p>
				<p class="h3">Top {{len(top_records)}} Records:</p>
				<table class="table">
					<thead>
						<tr>
							<th scope="col">Record</th>
							<th scope="col">Driver</th>
							<th scope="col">Minutes</th>
							<th scope="col">Date</th>
						</tr>
					</thead>
					<tbody>
						% for rid, did, name, minutes, date in top_records:
							<tr style="white-space: nowrap">
								<td><a href="/records/{{rid}}">{{rid}}</a></td>
								<td><a href="/drivers/{{did}}" class="text-truncate">{{name}}</a></td>
								<td>{{round(minutes, 3)}}</td>
								<td>{{date}}</td>
							</tr>
						% end
					</tbody>
				</table>
			</div>
			<div class="col-md-8 col-sm-6 col-xs-12">
				<%
					tabs = (
						("Records"           , "records"),
						("Individual Battles", "battles"),
						("Team Battles"      , "team-battles")
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
					<div class="tab-pane fade show active" id="records-pane">
						<table class="table">
							<thead>
								<tr>
									<th scope="col">Record</th>
									<th scope="col">Driver</th>
									<th scope="col">Minutes</th>
									<th scope="col">Date</th>
								</tr>
							</thead>
							<tbody>
								% for rid, did, name, minutes, date in all_records:
									<tr style="white-space: nowrap">
										<td><a href="/records/{{rid}}">{{rid}}</a></td>
										<td><a href="/drivers/{{did}}" class="text-truncate">{{name}}</a></td>
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
									<th scope="col">Driver 1</th>
									<th scope="col">Driver 2</th>
									<th scope="col">Result</th>
									<th scope="col">Date</th>
								</tr>
							</thead>
							<tbody>
								% for bid, did1, name1, did2, name2, min1, min2, date in all_battles:
									<tr style="white-space: nowrap">
										<td><a href="/battles/{{bid}}">{{bid}}</a></td>
										<td><a href="/drivers/{{did1}}" class="text-truncate">{{name1}}</a></td>
										<td><a href="/drivers/{{did2}}" class="text-truncate">{{name2}}</a></td>
										% if min1 == min2:
											<td>Draw</td>
										% elif min1 < min2:
											<td>Win For 1</td>
										% else:
											<td>Win For 2</td>
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
									<th scope="col">Winner</th>
									<th scope="col">Loser</th>
									<th scope="col">Date</th>
								</tr>
							</thead>
							<tbody>
								% for tbid, date, tid1, tname1, tid2, tname2, points1, points2 in all_team_battles:
									% wid, wname = (tid1, tname1) if points1 > points2 else (tid2, tname2)
									% lid, lname = (tid1, tname1) if points1 < points2 else (tid2, tname2)
									<tr style="white-space: nowrap">
										<td><a href="/team-battles/{{tbid}}">{{tbid}}</a></td>
										<td><a href="/teams/{{wid}}" class="text-truncate">{{wname}}</a></td>
										<td><a href="/teams/{{lid}}" class="text-truncate">{{lname}}</a></td>
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
