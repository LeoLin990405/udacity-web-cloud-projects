package com.udacity.project4.locationreminders.data

import com.udacity.project4.locationreminders.data.dto.ReminderDTO
import com.udacity.project4.locationreminders.data.dto.Result

// Test double for the local data source.
class FakeDataSource(
    private val reminders: MutableList<ReminderDTO> = mutableListOf()
) : ReminderDataSource {

    var shouldReturnError = false

    override suspend fun getReminders(): Result<List<ReminderDTO>> {
        return if (shouldReturnError) {
            Result.Error(TEST_ERROR_MESSAGE)
        } else {
            Result.Success(reminders.toList())
        }
    }

    override suspend fun saveReminder(reminder: ReminderDTO) {
        reminders.add(reminder)
    }

    override suspend fun getReminder(id: String): Result<ReminderDTO> {
        if (shouldReturnError) return Result.Error(TEST_ERROR_MESSAGE)

        reminders.firstOrNull { it.id == id }?.let {
            return Result.Success(it)
        }
        return Result.Error("Reminder not found!")
    }

    override suspend fun deleteAllReminders() {
        reminders.clear()
    }

    fun addReminders(vararg reminder: ReminderDTO) {
        reminders.addAll(reminder)
    }

    companion object {
        const val TEST_ERROR_MESSAGE = "Test exception"
    }
}
