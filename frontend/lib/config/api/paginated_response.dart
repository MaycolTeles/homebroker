class PaginatedResponse<T> {
  final int count;
  final String? next;
  final String? previous;
  final List<T> results;

  PaginatedResponse({
    required this.count,
    required this.next,
    required this.previous,
    required this.results,
  });

  factory PaginatedResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Map<String, dynamic>) fromJsonT,
  ) {
    var results =
        (json['results'] as List).map((item) => fromJsonT(item)).toList();

    return PaginatedResponse(
      count: json['count'],
      next: json['next'],
      previous: json['previous'],
      results: results,
    );
  }
}
