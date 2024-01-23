% include("bootstrap.tpl")

<title>Battle List | Project D</title>

<style>
	.main-container {
		background: url("/static/images/page-battle-list/background.png");
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
			<h1 class="display-1">Battle List</h1>
			<p><a href="/">Back To Main Page</a></p>
			<p>&nbsp;</p>
		</header>

		<table class="table">
			<thead>
				<tr>
					<th scope="col">Battle</th>
					<th scope="col">Driver 1</th>
					<th scope="col">Driver 2</th>
					<th scope="col">Course</th>
					<th scope="col">Result</th>
					<th scope="col">Date</th>
				</tr>
			</thead>
			<tbody>
				% for rid1, did1, cid1, date1, mins1, bid1, rid2, did2, _, _, mins2, _, dname1, dname2, cname in battles:
					<tr style="white-space: nowrap">
						<td><a href="/battles/{{bid1}}">{{bid1}}</a></td>
						<td><a href="/drivers/{{did1}}" class="text-truncate">{{dname1}}</a></td>
						<td><a href="/drivers/{{did2}}" class="text-truncate">{{dname2}}</a></td>
						<td><a href="/courses/{{cid1}}" class="text-truncate">{{cname}}</a></td>
						% if mins1 < mins2:
							<td>Win For 1</td>
						% elif mins1 > mins2:
							<td>Win For 2</td>
						% else:
							<td>Draw</td>
						% end
						<td>{{date1}}</td>
					</tr>
				% end
			</tbody>
		</table>
	</div>
</div>
