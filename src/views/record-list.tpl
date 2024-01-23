% include("bootstrap.tpl")

<title>Record List | Project D</title>

<style>
	.main-container {
		background: url("/static/images/page-record-list/background.png");
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
			<h1 class="display-1">Record List</h1>
			<p><a href="/">Back To Main Page</a></p>
			<p>&nbsp;</p>
		</header>

		<table class="table">
			<thead>
				<tr>
					<th scope="col">Record</th>
					<th scope="col">Driver</th>
					<th scope="col">Course</th>
					<th scope="col">Minutes</th>
					<th scope="col">Date</th>
				</tr>
			</thead>
			<tbody>
				% for id, did, cid, date, mins, bid, dname, cname in records:
					<tr style="white-space: nowrap">
						<td><a href="/records/{{id}}">{{id}}</a></td>
						<td><a href="/drivers/{{did}}" class="text-truncate">{{dname}}</a></td>
						<td><a href="/courses/{{cid}}" class="text-truncate">{{cname}}</a></td>
						<td>{{round(mins, 3)}}</td>
						<td>{{date}}</td>
					</tr>
				% end
			</tbody>
		</table>
	</div>
</div>
