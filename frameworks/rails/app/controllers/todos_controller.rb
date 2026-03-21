class TodosController < ApplicationController
  def index
    render json: Todo.all.order(:id)
  end

  def create
    todo = Todo.create!(title: params[:title], done: params[:done] || false)
    render json: todo, status: :created
  end
end
